import sys
Q_WS_MAC=Q_OS_MAC=sys.platform=='darwin'

from optparse import OptionParser

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *

DEFAULT_VOLUME=-1.0

class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.playButton=0
        self.nextEffect=0
        self.settingsDialog=SettingsDialog()
        self.m_AudioOutput=Phonon.AudioOutput(Phonon.VideoCategory)
        self.m_videoWidget=MediaVideoWidget(self)
        self.m_videoWindow=QWidget()
        self.m_MediaObject=Phonon.MediaObject()

        self.setWindowTitle("Media Player")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.m_videoWidget.setContextMenuPolicy(Qt.CustomContextMenu)

        buttonSize=QSize(34, 28)

        openButton=QPushButton(self)
        openButton.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))

        bpal=QPalette()
        arrowColor=bpal.buttonText().color()
        if arrowColor==Qt.black: arrowColor=QColor(80,80,80)
        bpal.setBrush(QPalette.ButtonText, arrowColor)
        openButton.setPalette(bpal)

        self.rewindButton=QPushButton(self)
        self.rewindButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))

        self.forwardButton=QPushButton(self)
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.forwardButton.setEnabled(False)

        self.playButton=QPushButton(self)
        self.playIcon=self.style().standardIcon(QStyle.SP_MediaPlay)
        self.pauseIcon=self.style().standardIcon(QStyle.SP_MediaPause)
        self.playButton.setIcon(self.playIcon)

        self.slider=Phonon.SeekSlider(self)
        self.slider.setMediaObject(self.m_MediaObject)

        self.volume=Phonon.VolumeSlider(self.m_AudioOutput)

        vLayout=QVBoxLayout(self)
        vLayout.setContentsMargins(8, 8, 8, 8)

        layout=QHBoxLayout()

        self.info=QLabel(self)
        self.info.setMinimumHeight(70)
        self.info.setAcceptDrops(False)
        self.info.setMargin(2)
        self.info.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.info.setLineWidth(2)
        self.info.setAutoFillBackground(True)

        palette=QPalette()
        palette.setBrush(QPalette.WindowText, Qt.white)

        if not Q_WS_MAC:
            openButton.setMinimumSize(54, buttonSize.height())
            self.rewindButton.setMinimumSize(buttonSize)
            self.forwardButton.setMinimumSize(buttonSize)
            self.playButton.setMinimumSize(buttonSize)

        self.info.setStyleSheet("QLabel { border-image:url(./screen.png); border-width:3px; }")
        self.info.setPalette(palette)
        self.info.setText("<center>No media</center>")

        self.volume.setFixedWidth(120)

        layout.addWidget(openButton)
        layout.addWidget(self.rewindButton)
        layout.addWidget(self.playButton)
        layout.addWidget(self.forwardButton)
        layout.addStretch()
        layout.addWidget(self.volume)

        vLayout.addWidget(self.info)
        self.initVideoWindow()
        vLayout.addWidget(self.m_videoWindow)
        buttonPanelLayout=QVBoxLayout()
        self.m_videoWindow.hide()
        buttonPanelLayout.addLayout(layout)

        self.timeLabel=QLabel(self)
        self.progressLabel=QLabel(self)

        sliderPanel=QWidget(self)
        sliderLayout=QHBoxLayout()
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(self.timeLabel)
        sliderLayout.addWidget(self.progressLabel)
        sliderLayout.setContentsMargins(0, 0, 0, 0)
        sliderPanel.setLayout(sliderLayout)

        buttonPanelLayout.addWidget(sliderPanel)
        buttonPanelLayout.setContentsMargins(0, 0, 0, 0)

        if Q_OS_MAC:
            layout.setSpacing(4)
            buttonPanelLayout.setSpacing(0)
            self.info.setMinimumHeight(100)
            self.info.setFont(QFont("verdana", 15))
            openButton.setFocusPolicy(Qt.NoFocus)

        buttonPanelWidget=QWidget(self)
        buttonPanelWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        buttonPanelWidget.setLayout(buttonPanelLayout)
        vLayout.addWidget(buttonPanelWidget)

        labelLayout=QHBoxLayout()
        vLayout.addLayout(labelLayout)

        self.setLayout(vLayout)

        self.fileMenu=QMenu(self)
        openFileAction=self.fileMenu.addAction("Open &File...")
        openUrlAction=self.fileMenu.addAction("Open &Location...")

        openLinkAction=self.fileMenu.addAction("Open &RAM File...")
        openLinkAction.triggered.connect(self.openRamFile)

        self.fileMenu.addSeparator()
        aspectMenu=self.fileMenu.addMenu("&Aspect Ratio")
        aspectGroup=QActionGroup(aspectMenu)
        aspectGroup.triggered.connect(self.aspectChanged)
        aspectGroup.setExclusive(True)

        aspectActionAuto=aspectMenu.addAction("Auto")
        aspectActionAuto.setCheckable(True)
        aspectActionAuto.setChecked(True)
        aspectGroup.addAction(aspectActionAuto)

        aspectActionScale=aspectMenu.addAction("Scale")
        aspectActionScale.setCheckable(True)
        aspectGroup.addAction(aspectActionScale)

        aspectAction16_9=aspectMenu.addAction("16:9")
        aspectAction16_9.setCheckable(True)
        aspectGroup.addAction(aspectAction16_9)

        aspectAction4_3=aspectMenu.addAction("4:3")
        aspectAction4_3.setCheckable(True)
        aspectGroup.addAction(aspectAction4_3)

        scaleMenu=self.fileMenu.addMenu("&Scale Mode")
        scaleGroup=QActionGroup(scaleMenu)
        scaleGroup.triggered.connect(self.scaleChanged)
        scaleGroup.setExclusive(True)
        
        scaleActionFit=scaleMenu.addAction("Fit In View")
        scaleActionFit.setCheckable(True)
        scaleActionFit.setChecked(True)
        scaleGroup.addAction(scaleActionFit)

        scaleActionCrop=scaleMenu.addAction("Scale and Crop")
        scaleActionCrop.setCheckable(True)
        scaleGroup.addAction(scaleActionCrop)

        self.m_fullScreenAction=self.fileMenu.addAction("Full screen Video")
        self.m_fullScreenAction.setCheckable(True)
        self.m_fullScreenAction.setEnabled(False)
        self.m_fullScreenAction.toggled.connect(self.m_videoWidget.setFullScreen)
        self.m_videoWidget.fullScreenChanged.connect(self.m_fullScreenAction.setChecked)

        self.fileMenu.addSeparator()
        settingsAction=self.fileMenu.addAction("&Settings...")

        self.rewindButton.clicked.connect(self.rewind)
        openButton.setMenu(self.fileMenu)
        self.playButton.clicked.connect(self.playPause)
        self.forwardButton.clicked.connect(self.forward)
        settingsAction.triggered.connect(self.showSettingsDialog)
        openUrlAction.triggered.connect(self.openUrl)
        openFileAction.triggered.connect(self.openFile)

        self.m_videoWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.m_MediaObject.metaDataChanged.connect(self.updateInfo)
        self.m_MediaObject.totalTimeChanged.connect(self.updateTime)
        self.m_MediaObject.tick.connect(self.updateTime)
        self.m_MediaObject.finished.connect(self.finished)
        self.m_MediaObject.stateChanged.connect(self.stateChanged)
        self.m_MediaObject.bufferStatus.connect(self.bufferStatus)
        self.m_MediaObject.hasVideoChanged.connect(self.videoChanged)

        self.rewindButton.setEnabled(False)
        self.playButton.setEnabled(False)
        self.setAcceptDrops(True)

        self.m_audioOutputPath=Phonon.createPath(self.m_MediaObject, self.m_AudioOutput)
        Phonon.createPath(self.m_MediaObject, self.m_videoWidget)

        self.initSettingsDialog()
        self.resize(self.minimumSizeHint())

    def stateChanged(self, newstate, oldstate):
        if oldstate==Phonon.LoadingState:
            videoHintRect=QRect(QPoint(0,0), self.m_videoWidget.sizeHint())
            newVideoRect=QApplication.desktop().screenGeometry().intersected(videoHintRect)

            if not self.m_smallScreen:
                if self.m_MediaObject.hasVideo(): 
                    QApplication.processEvents()
                    self.resize(self.sizeHint())
                else: self.resize(self.minimumSize())

        if newstate==Phonon.ErrorState:
            if self.m_MediaObject.errorType()==Phonon.FatalError:
                self.playButton.setEnabled(False)
                self.rewindButton.setEnabled(False)
            else: self.m_MediaObject.pause()
            QMessageBox.warning(self, "Media Player", self.m_MediaObject.errorString(), QMessageBox.Close)
            return

        if newstate==Phonon.StoppedState: self.m_videoWidget.setFullScreen(False)

        if newstate in (Phonon.StoppedState, Phonon.PausedState):
            self.playButton.setIcon(self.playIcon)
            if self.m_MediaObject.currentSource().type()!=Phonon.MediaSource.Invalid:
                self.playButton.setEnabled(True)
                self.rewindButton.setEnabled(True)
            else:
                self.playButton.setEnabled(False)
                self.rewindButton.setEnabled(False)
            return

        if newstate==Phonon.PlayingState:
            self.playButton.setEnabled(True)
            self.playButton.setIcon(self.pauseIcon)
            if self.m_MediaObject.hasVideo(): self.m_videoWindow.show()
            
        if newstate in (Phonon.PlayingState, Phonon.BufferingState):
            self.rewindButton.setEnabled(True)
            return

        if newstate==Phonon.LoadingState: self.rewindButton.setEnabled(True)

    def initSettingsDialog(self):
        s=self.settingsDialog
        s.brightnessSlider.valueChanged.connect(self.setBrightness)
        s.hueSlider.valueChanged.connect(self.setHue)
        s.saturationSlider.valueChanged.connect(self.setSaturation)
        s.contrastSlider.valueChanged.connect(self.setContrast)
        s.aspectCombo.currentIndexChanged.connect(self.setAspect)
        s.scalemodeCombo.currentIndexChanged.connect(self.setScale)
        s.effectButton.clicked.connect(self.configureEffect)

        s.brightnessSlider.setValue(int(self.m_videoWidget.brightness()*8))
        s.hueSlider.setValue(int(self.m_videoWidget.hue()*8))
        s.saturationSlider.setValue(int(self.m_videoWidget.saturation()*8))
        s.contrastSlider.setValue(int(self.m_videoWidget.contrast()*8))
        s.aspectCombo.setCurrentIndex(self.m_videoWidget.aspectRatio())
        s.scalemodeCombo.setCurrentIndex(self.m_videoWidget.scaleMode())

        for i, device in enumerate(Phonon.BackendCapabilities.availableAudioOutputDevices()):
            itemText=device.name()
            if not device.description().isEmpty(): itemText+=" ("+device.description()+")"
            s.deviceCombo.addItem(itemText)
            if device==self.m_AudioOutput.outputDevice(): s.deviceCombo.setCurrentIndex(i)

        s.audioEffectsCombo.addItem("<no effect>")

        currEffects=self.m_audioOutputPath.effects()
        currEffect=currEffects[0] if len(currEffects) else None
        for i, effect in enumerate(Phonon.BackendCapabilities.availableAudioEffects()):
            s.audioEffectsCombo.addItem(effect.name())
            if currEffect and effect==currEffect.description(): s.audioEffectsCombo.setCurrentIndex(i)
        s.audioEffectsCombo.currentIndexChanged.connect(self.effectChanged)

    def setVolume(self, volume): self.m_AudioOutput.setVolume(volume)

    def setSmallScreen(self, smallScreen): self.m_smallScreen=smallScreen

    def effectChanged(self):
        currIndex=self.settingsDialog.audioEffectsCombo.currentIndex()
        if currIndex:
            availableEffects=Phonon.BackendCapabilities.availableAudioEffects()
            chosenEffect=availableEffects[currIndex-1]

            currEffects=self.m_audioOutputPath.effects()
            currEffect=currEffects[0] if len(currEffects) else None

            if self.nextEffect and not (currEffect and (currentEffect.description().name()==self.nextEffect.description().name())):
                del self.nextEffect

            self.nextEffect=Phonon.Effect(chosenEffect)
        self.settingsDialog.effectButton.setEnabled(currIndex) 

    def showSettingsDialog(self):
        hasPausedForDialog=self.playPauseForDialog()

        oldBrightness=self.m_videoWidget.brightness()
        oldHue=self.m_videoWidget.hue()
        oldSaturation=self.m_videoWidget.saturation()
        oldContrast=self.m_videoWidget.contrast()
        oldAspect=self.m_videoWidget.aspectRatio()
        oldScale=self.m_videoWidget.scaleMode()
        currentEffect=self.settingsDialog.audioEffectsCombo.currentIndex()

        if self.settingsDialog.exec_():
            self.m_MediaObject.setTransitionTime(int(1000.0*float(self.settingsDialog.crossFadeSlider.value())/2.0))
            devices=Phonon.BackendCapabilities.availableAudioOutputDevices()
            self.m_AudioOutput.setOutputDevice(devices[self.settingsDialog.deviceCombo.currentIndex()])
            currEffects=self.m_audioOutputPath.effects()

            if self.settingsDialog.audioEffectsCombo.currentIndex():
                currEffect=currEffects[0] if len(currEffects) else None
                if not currentEffect or (currEffect.description()!=self.nextEffect.description()):
                    for effect in currEffects: self.m_audioOutputPath.removeEffect(effect)
            else:
                for effect in currEffects: self.m_audioOutputPath.removeEffect(effect)
                self.nextEffect=None
        else:
            self.m_videoWidget.setBrightness(oldBrightness)
            self.m_videoWidget.setHue(oldHue)
            self.m_videoWidget.setSaturation(oldSaturation)
            self.m_videoWidget.setContrast(oldContrast)
            self.m_videoWidget.setAspectRatio(oldAspect)
            self.m_videoWidget.setScaleMode(oldScale)
            self.settingsDialog.audioEffectsCombo.setCurrentIndex(currentEffect)

        if hasPausedForDialog: self.m_MediaObject.play()

    def initVideoWindow(self):
        videoLayout=QVBoxLayout()
        videoLayout.addWidget(self.m_videoWidget)
        videoLayout.setContentsMargins(0, 0, 0, 0)
        self.m_videoWindow.setLayout(videoLayout)
        self.m_videoWindow.setMinimumSize(100,100)

    def configureEffect(self):
        if not self.nextEffect: return

        currEffects=self.m_audioOutputPath.effects()
        availableEffects=Phonon.BackendCapabilities.availableAudioEffects()

        choseEffectIndex=self.settingsDialog.audioEffectsCombo.currentIndex()
        if choseEffectIndex:
            chosenEffect=availableEffects[choseEffectIndex-1]

            effectDialog=QDialog()
            effectDialog.setWindowTitle("Configure Effect")
            
            topLayout=QVBoxLayout(effectDialog)
            description=QLabel("<b>Description:</b><br />"+chosenEffect.description(), effectDialog)
            description.setWordWrap(True)
            topLayout.addWidget(description)

            scrollArea=QScrollArea(effectDialog)
            topLayout.addWidget(scrollArea)

            savedParams=[self.nextEffect.parameterValue(param) for param in self.nextEffect.parameters()]
            
            scrollWidget=Phonon.EffectWidget(self.nextEffect)
            scrollWidget.setMinimumWidth(320)
            scrollWidget.setContentsMargins(10, 10, 10, 10)
            scrollArea.setWidget(scrollWidget)

            bbox=QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, parent=effectDialog)
            bbox.accepted.connect(effectDialog.accept)
            bbox.rejected.connect(effectDialog.reject)
            topLayout.addWidget(bbox)

            if not effectDialog.exec_():
                for i, param in enumerate(self.nextEffect.parameters()): self.nextEffect.setParameterValue(param, savedParams[i])

    def handleDrop(self, e):
        urls=e.mimeData().urls()
        if e.proposedAction()==Qt.MoveAction:
            for url in urls: self.m_MediaObject.enqueue(Phonon.MediaSource(url.toLocalFile()))
        else:
            self.m_MediaObject.clearQueue()
            if len(urls)>0:
                fileName=urls[0].toLocalFile()
                dir=QDir(fileName)
                if dir.exists():
                    dir.setFilter(QDir.Files)
                    entries=dir.entryList()
                    if len(entries)>0:
                        self.setFile(fileName+QDir.seperator()+entries[0])
                        for entry in entries: self.m_MediaObject.enqueue(fileName+QDir.seperator()+entry)
                else:
                    self.setFile(fileName)
                    for url in urls: self.m_MediaObject.enqueue(Phonon.MediaSource(url.toLocalFile()))

        self.forwardButton.setEnabled(len(self.m_MediaObject.queue())>0)
        self.m_MediaObject.play()
                        
    def dropEvent(self, e):
        if e.mimeData().hasUrls() and e.proposedAction()!=Qt.LinkAction:
            e.acceptProposedAction()
            self.handleDrop(e)
        else: e.ignore()

    def dragEnterEvent(self, e): self.dragMoveEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            if e.proposedAction() in (Qt.CopyAction, Qt.MoveAction):
                e.acceptProposedAction()

    def playPause(self):
        if self.m_MediaObject.state()==Phonon.PlayingState: self.m_MediaObject.pause()
        else:
            if self.m_MediaObject.currentTime()==self.m_MediaObject.totalTime(): self.m_MediaObject.seek(0)
            self.m_MediaObject.play()

    def setFile(self, fileName):
        self.setWindowTitle(fileName.split('/')[-1])
        self.m_MediaObject.setCurrentSource(Phonon.MediaSource(fileName))
        self.m_MediaObject.play()

    def setLocation(self, location):
        self.setWindowTitle(location.split('/')[-1])
        self.m_MediaObject.setCurrentSource(Phonon.MediaSource(QUrl.fromEncoded(location.toUtf8())))
        self.m_MediaObject.play()

    def playPauseForDialog(self):
        if self.m_smallScreen and self.m_MediaObject.hasVideo():
            if self.m_MediaObject.state()==Phonon.PlayingState:
                self.m_MediaObject.pause()
                return True
        return False

    def openFile(self): 
        hasPausedForDialog=self.playPauseForDialog()

        fileNames=QFileDialog.getOpenFileNames(self, "", QDesktopServices.storageLocation(QDesktopServices.MusicLocation))
        
        if hasPausedForDialog: self.m_MediaObject.play()

        self.m_MediaObject.clearQueue()
        if len(fileNames)>0:
            self.setFile(fileNames[0])
            for i in range(1,len(fileNames)): self.m_MediaObject.enqueue(Phonon.MediaSource(fileNames[i]))

        self.forwardButton.setEnabled(len(self.m_MediaObject.queue())>0)

    def bufferStatus(self, percent):        
        self.progressLabel.setText("" if percent==100 else ("%d" % percent))

    def setSaturation(self, saturation): self.m_videoWidget.setSaturation(saturation/8.0)

    def setHue(self, hue): self.m_videoWidget.setHue(hue/8.0)

    def setAspect(self, aspect): self.m_videoWidget.setAspectRatio(Phonon.VideoWidget.AspectRatio(aspect))

    def setScale(self, scale): self.m_videoWidget.setScaleMode(Phonon.VideoWidget.ScaleMode(scale))

    def setBrightness(self, brightness): self.m_videoWidget.setBrightness(brightness/8.0)
    
    def setContrast(self, contrast): self.m_videoWidget.setContrast(contrast/8.0)

    def updateInfo(self):
        maxLength=30
        font="<font color=\"#ffeeaa\">"
        fontmono="<font family=\"monospace,courier new\" color=\"#ffeeaa\">"

        metaData=self.m_MediaObject.metaData()

        trackArtist=str(metaData.get(QString('ARTIST'), ["[No Artist]"])[0])
        if len(trackArtist)>maxLength: trackArtist=trackArtist[:maxLength]+"..."
        trackArtist="Artist: %s%s</font>" % (font, trackArtist)

        trackTitle=str(metaData.get(QString('TITLE'), ["[No Title]"])[0])
        if len(trackTitle)>maxLength: trackTitle=trackTitle[:maxLength]+"..."
        trackTitle="Title: %s%s<br></font>" % (font, trackTitle)

        trackBitrate=int(str(metaData.get(QString('BITRATE'), ["0"])[0]))
        bitrate="<br>Bitrate: %s%dkbit</font>" % (font, trackBitrate/1000) if trackBitrate!=0 else ""

        if self.m_MediaObject.currentSource().type()==Phonon.MediaSource.Url:
            fileName=str(self.m_MediaObject.currentSource().url().toString())
        else:
            fileName=str(self.m_MediaObject.currentSource().fileName().split('/')[-1])
        if len(fileName)>maxLength: fileName=fileName[:maxLength]+"..."

        self.info.setText(trackTitle+trackArtist+bitrate)

    def updateTime(self):
        _len=self.m_MediaObject.totalTime()
        _pos=self.m_MediaObject.currentTime()

        timeString=""
        if _pos or _len:
            _sec=_pos/1000
            _min=_sec/60
            _hour=_min/60
            _msec=_pos
            playTime=QTime(_hour%60, _min%60, _sec%60, _msec%1000)
            
            _sec=_len/1000
            _min=_sec/60
            _hour=_min/60
            _msec=_len
            stopTime=QTime(_hour%60, _min%60, _sec%60, _msec%1000)

            timeFormat="h:mm:ss" if _hour>0 else "m:ss"
            timeString=playTime.toString(timeFormat)
            if _len: timeString+='/'+stopTime.toString(timeFormat)

        self.timeLabel.setText(timeString)

    def rewind(self): self.m_MediaObject.seek(0)

    def forward(self):
        queue=self.m_MediaObject.queue()
        if len(queue)>0:
            self.m_MediaObject.setCurrentSource(queue[0])
            self.forwardButton.setEnabled(len(queue)>1)
            self.m_MediaObject.play()

    def openUrl(self):
        settings=QSettings()
        settings.beginGroup("BrowserMainWindow")
        sourceUrl=str(settings.value("location").toString())

        sourceUrl,ok=QInputDialog.getText(self, "Open Location", "Please enter a valid address here:", QLineEdit.Normal, sourceUrl)
        if ok and not sourceUrl.isEmpty():
            self.setLocation(sourceUrl)
            settings.value("location", sourceUrl)

    def openRamFile(self): pass

    def finished(self): pass

    def showContextMenu(self, point): self.fileMenu.popup(point if self.m_videoWidget.isFullScreen() else self.mapToGlobal(point))

    def aspectChanged(self, action):
        text=str(action.text())
        if text=="16:9": self.m_videoWidget.setAspectRatio(Phonon.VideoWidget.AspectRatio16_9)
        elif text=="4:3": self.m_videoWidget.setAspectRatio(Phonon.VideoWidget.AspectRatio4_3)
        elif text=="Scale": self.m_videoWidget.setAspectRatio(Phonon.VideoWidget.AspectRatioWidget)
        else: self.m_videoWidget.setAspectRatio(Phonon.VideoWidget.AspectRatioAuto)

    def scaleChanged(self, action):
        if str(action.text())=="Scale and Crop": self.m_videoWidget.setScaleMode(Phonon.VideoWidget.ScaleAndCrop)
        else: self.m_videoWidget.setScaleMode(Phonon.VideoWidget.FitInView)

    def videoChanged(self, status):
        self.info.setVisible(not status)
        self.m_videoWindow.setVisible(status)
        self.m_fullScreenAction.setEnabled(status)

class MediaVideoWidget(Phonon.VideoWidget):
    fullScreenChanged=pyqtSignal(bool)
    def __init__(self, player=0, parent=None):
        Phonon.VideoWidget.__init__(self, parent)

        self.m_player=player

        self.m_action=QAction(self)
        self.m_action.setCheckable(True);
        self.m_action.setChecked(False);
        self.m_action.setShortcut(QKeySequence(Qt.AltModifier+Qt.Key_Return))
        self.m_action.setShortcutContext(Qt.WindowShortcut)
        self.m_action.toggled.connect(self.setFullScreen)
        self.addAction(self.m_action)

        self.m_timer=QBasicTimer()

        self.setAcceptDrops(True)

    def setFullScreen(self, enabled):
        Phonon.VideoWidget.setFullScreen(self, enabled)
        self.fullScreenChanged.emit(enabled)

    def mouseDoubleClickEvent(self, e):
        Phonon.VideoWidget.mouseDoubleClickEvent(self, e)
        self.setFullScreen(not self.isFullScreen())

    def keyPressEvent(self, e):
        if not e.modifiers():
            if e.key()==Qt.Key_Space:
                self.m_player.playPause()
                e.accept()
                return
            elif e.key() in (Qt.Key_Escape, Qt.Key_Backspace):
                self.setFullScreen(False)
                e.accept()
                return
        Phonon.VideoWidget.keyPressEvent(self, e)

    def event(self, e):
        if e.type()==QEvent.Close:
            e.ignore()
            return True
        elif e.type() in (QEvent.MouseMove, QEvent.WindowStateChange):
            if e.type()==QEvent.MouseMove: self.unsetCursor()
            self.m_action.setChecked(self.windowState() and Qt.WindowFullScreen)
            if self.windowState() and Qt.WindowFullScreen: self.m_timer.start(1000, self)
            else: self.m_timer.stop()

        return Phonon.VideoWidget.event(self, e)

    def timerEvent(self, e):
        if e.timerId()==self.m_timer.timerId(): self.setCursor(Qt.BlankCursor)
        return Phonon.VideoWidget.timerEvent(self, e)

    def dropEvent(self, e): self.m_player.handleDrop(e)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)

        QVBoxLayout(self)

        groupBox1=QGroupBox("Video Options:", self)
        groupBox1.setLayout(QGridLayout())

        groupBox1.layout().addWidget(QLabel("Contrast:", self), 0, 0)
        self.contrastSlider=QSlider(Qt.Horizontal, self)
        self.contrastSlider.setRange(-8, 8)
        self.contrastSlider.setPageStep(10)
        self.contrastSlider.setSingleStep(1)
        self.contrastSlider.setTickPosition(QSlider.TicksBelow)
        self.contrastSlider.setTickInterval(4)
        groupBox1.layout().addWidget(self.contrastSlider, 0, 1)

        groupBox1.layout().addWidget(QLabel("Brightness:", self), 1, 0)
        self.brightnessSlider=QSlider(Qt.Horizontal, self)
        self.brightnessSlider.setRange(-8, 8)
        self.brightnessSlider.setPageStep(10)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setTickPosition(QSlider.TicksBelow)
        self.brightnessSlider.setTickInterval(4)
        groupBox1.layout().addWidget(self.brightnessSlider, 1, 1)

        groupBox1.layout().addWidget(QLabel("Saturation:", self), 2, 0)
        self.saturationSlider=QSlider(Qt.Horizontal, self)
        self.saturationSlider.setRange(-8, 8)
        self.saturationSlider.setPageStep(10)
        self.saturationSlider.setSingleStep(1)
        self.saturationSlider.setTickPosition(QSlider.TicksBelow)
        self.saturationSlider.setTickInterval(4)
        groupBox1.layout().addWidget(self.saturationSlider, 2, 1)

        groupBox1.layout().addWidget(QLabel("Hue:", self), 3, 0)
        self.hueSlider=QSlider(Qt.Horizontal, self)
        self.hueSlider.setRange(-8, 8)
        self.hueSlider.setPageStep(10)
        self.hueSlider.setSingleStep(1)
        self.hueSlider.setTickPosition(QSlider.TicksBelow)
        self.hueSlider.setTickInterval(4)
        groupBox1.layout().addWidget(self.hueSlider, 3, 1)

        groupBox1.layout().addWidget(QLabel("Aspect Ratio:", self), 4, 0)
        self.aspectCombo=QComboBox()
        groupBox1.layout().addWidget(self.aspectCombo, 4, 1)

        groupBox1.layout().addWidget(QLabel("Scale Mode:", self), 5, 0)
        self.scalemodeCombo=QComboBox()
        groupBox1.layout().addWidget(self.scalemodeCombo, 5, 1)

        self.layout().addWidget(groupBox1)

        groupBox2=QGroupBox("Audio Options:", self)
        groupBox2.setLayout(QGridLayout())

        groupBox2.layout().addWidget(QLabel("Audio Device:", self), 0, 0)
        self.deviceCombo=QComboBox()
        groupBox2.layout().addWidget(self.deviceCombo, 0, 1, 1, 2)

        groupBox2.layout().addWidget(QLabel("Audio Effect:", self), 1, 0)
        self.audioEffectsCombo=QComboBox()
        groupBox2.layout().addWidget(self.audioEffectsCombo, 1, 1)
        self.effectButton=QToolButton()
        self.effectButton.setText("Setup")
        groupBox2.layout().addWidget(self.effectButton, 1, 2)

        groupBox2.layout().addWidget(QLabel("Cross Fade:", self), 2, 0, 2, 1, Qt.AlignTop)
        self.crossFadeSlider=QSlider(Qt.Horizontal, self)
        self.crossFadeSlider.setRange(-20, 20)
        self.crossFadeSlider.setPageStep(2)
        self.crossFadeSlider.setSingleStep(1)
        self.crossFadeSlider.setTickPosition(QSlider.TicksBelow)
        self.crossFadeSlider.setTickInterval(0)
        groupBox2.layout().addWidget(self.crossFadeSlider, 2, 1, 1, 2)

        labelLayout=QHBoxLayout()

        labelLayout.addWidget(QLabel("-10 sec", self))
        labelLayout.addStretch()
        labelLayout.addWidget(QLabel("0", self))
        labelLayout.addStretch()
        labelLayout.addWidget(QLabel(" 10 sec", self))

        groupBox2.layout().addLayout(labelLayout, 3, 1, 1, 2)

        self.layout().addWidget(groupBox2)

        buttonBox=QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout().addWidget(buttonBox)

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    a.setStyle("Cleanlooks")
    a.setApplicationName("Media Player")
    a.setOrganizationName("BAE Systems")
    a.setQuitOnLastWindowClosed(True)

    parser=OptionParser(usage="usage: %prog [options] media-file")
    parser.add_option("-s", "--small-screen", dest="smallScreen", action="store_true", default=False, help="run in small screen mode")
    parser.add_option("-v", "--volume", dest="volume", type=float, default=DEFAULT_VOLUME, help="default volume")
    options, args=parser.parse_args(argv)
    fileName=None if len(args)<2 else argv[1]

    player=MediaPlayer()
    player.setSmallScreen(options.smallScreen)
    if options.volume!=DEFAULT_VOLUME: player.setVolume(options.volume)
    if fileName: player.setFile(fileName)

    if options.smallScreen: player.showMaximized()
    else: player.show()

    exit(a.exec_())

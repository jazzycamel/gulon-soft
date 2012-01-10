<!-- Copyright (c) GulonSoft 2011 -->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>GulonSoft</title>
    <link rel="shortcut icon" href="favicon.ico" />
    <link rel="stylesheet" type="text/css" href="media/master.css" />
    <link rel="stylesheet" type="text/css" href="media/jquery-ui-1.8.14/development-bundle/themes/custom-theme/jquery.ui.all.css" />
    <?php
      if($extraStyle){ echo $extraStyle; }
    ?>
    <script type="text/javascript" src="media/roundies.js"></script>
    <script type="text/javascript" src="media/jquery-1.5.1.min.js"></script>
    <script type="text/javascript" src="media/jquery-ui-1.8.14/development-bundle/ui/jquery.ui.core.js"></script>
    <script type="text/javascript" src="media/jquery-ui-1.8.14/development-bundle/ui/jquery.ui.widget.js"></script>
    <script type="text/javascript" src="media/jquery-ui-1.8.14/development-bundle/ui/jquery.ui.accordion.js"></script>
    <script type="text/javascript" src="media/master.js"></script>
    <?php
      if($extraScript){ echo $extraScript; }
    ?>
    <!--<base href="http://www.gulon.co.uk/" />-->
    <base href="http://localhost:8888/gulon/" />
  </head>
  <body>
    <div id="page">
      <div id="mastHead">
        <div id="mastHeadTop" class="greyOnGrey">
          <a href="" class="headLink">gulon.co.uk</a><span id="subHead">the home of GulonSoft</span>
        </div>
        <div id="mastHeadBottom" class="whiteOnGreen">
          <a href="" class="boxLink">HOME</a>
          <a href="code.php" class="boxLink">CODE</a>
          <a href="projects.php" class="boxLink">PROJECTS</a>
          <a href="contact.php" class="boxLink">CONTACT</a>
        </div>
      </div>
      <div id="pageContainer" class="blackOnWhite">

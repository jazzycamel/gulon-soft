/* First we define the namespaces, the so called "Namespaces”, are in simple words,
libraries of required data.
For example almost every C# program starts with the namespace "System", in the
following case we will use these namespaces: System, System.Drawing, System.Net, System.Text,
System.Windows.Forms. Each one of them speaks for its purpose clearly.
*/
using System;
using System.Drawing;
using System.Net;
using System.Text;
using System.Windows.Forms;

/* Now we start the program with the "class" which we name "AsyncResolve". Note that after the
* class we have the ":" identificator and then the word "Form". This means: "the object AsyncResolve
* will create a Windows dialog/form/ */
public class AsyncResolve : Form
{
/* Here we define the boxes which are in the case the very main objects in the application
thus we better define them early */
TextBox address;
ListBox results;

/* Here we use the "AsyncCallback" delegate, whose function is to start the Asynchronous
* web services in our program. Actually this object is very important for the program, but
* doesn't appear often, because we just define it and later use it in our main class, as shown
* below */
private AsyncCallback OnResolved;

/* Below is The "main" class of program. Take a look at the word "AsyncResolve". This once again
* should remind you that we use a predefined words (called "DELEGATES") in our program which
* actually initiate the C# functionality by default. In simple words, when we use such predefined delegates
* we simply instruct the C# environment to accomplish the entire job. In the case our
* desired job is to resolve a web address such as "ebay.com" onto its actual IP address (
* say...64.127.34.98.*/
public AsyncResolve()
{
/* Here we define the Text box and later on the string "
OnResolved = new AsyncCallback(Resolved);" we invoke the object/delegate defined earlier: "AsyncCallback".
* In simple words we earlier invoked the needed object/function that performs
* the hard task: Getting the IP. Now we just include this object(AsyncCallback in our
* textbox to connect it with the text box */
Text = "Website to IP";
Size = new Size(400, 380);
OnResolved = new AsyncCallback(Resolved);

/* Here we define and connect the graphical parts of our program. Such as the listbox,
the button, the text. It is all accomplished here in several lines */

Label label1 = new Label();
label1.Parent = this;
label1.Text = "Enter website to find its IP:";
label1.AutoSize = true;
label1.Location = new Point(10, 10);

address = new TextBox();
address.Parent = this;
address.Size = new Size(200, 2 * Font.Height);
address.Location = new Point(10, 35);

results = new ListBox();
results.Parent = this;
results.Location = new Point(10, 65);
results.Size = new Size(350, 20 * Font.Height);

Button checkit = new Button();
checkit.Parent = this;
checkit.Text = "Find IP";
checkit.Location = new Point(235, 32);
checkit.Size = new Size(7 * Font.Height, 2 * Font.Height);
checkit.Click += new EventHandler(ButtonResolveOnClick);
}

/* Here we simply tell the program what must happen when the button is clicked.
* Obviously in the following case, what happens is that when the button is clicked
* we invoke a method called "Dns.BeginResolve" which actually finished the real task started
* by the AsyncCallback delegate, which is to
* find the IP address of the website */
void ButtonResolveOnClick(object obj, EventArgs ea)
{
results.Items.Clear();
string addr = address.Text;
Object state = new Object();

Dns.BeginResolve(addr, OnResolved, state);
}

/* Now we must show the found data. We use the keyword "string" to group the data in lines.
along with the objects of the DNS resolving */
private void Resolved(IAsyncResult ar)
{
string buffer;

IPHostEntry iphe = Dns.EndResolve(ar);

buffer = "Host name: " + iphe.HostName;
results.Items.Add(buffer);

foreach (string alias in iphe.Aliases)
{
buffer = "Alias: " + alias;
results.Items.Add(buffer);
}
foreach (IPAddress addrs in iphe.AddressList)
{
buffer = "IP: " + addrs.ToString();
results.Items.Add(buffer);
}
}

/* Here in the last class we simply use the required Main() method, which is required
* in every C# application. Hence, we use the Main() method and instruct it to start the
* application along with the object/delegate "AsyncResolve" */
public static void Main()
{
Application.Run(new AsyncResolve());
}
}
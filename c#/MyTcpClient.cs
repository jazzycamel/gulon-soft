using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Diagnostics;

namespace tcpClient
{
    class MyTcpClient
    {
        private TcpClient _client;
        private IPAddress _address;
        private int _port;
        private IPEndPoint _endPoint;
        private bool _disposed;

        public MyTcpClient(IPAddress adress, int port)
        {
            _address = adress;
            _port = port;
            _endPoint = new IPEndPoint(_address, _port);
        }

        public void ConnectToServer(string msg)
        {
            try
            {
                _client = new TcpClient();
                _client.Connect(_endPoint);

                byte[] bytes = Encoding.ASCII.GetBytes(msg);

                using (NetworkStream ns = _client.GetStream())
                {
                    Trace.WriteLine("Sending message to server: " + msg);
                    ns.Write(bytes, 0, bytes.Length);

                    bytes = new byte[1024];

                    int bytesRead = ns.Read(bytes, 0, bytes.Length);
                    string serverResponse = Encoding.ASCII.GetString(bytes, 0, bytesRead);

                    Trace.WriteLine("Server said: " + serverResponse);
                }
            }

            catch (SocketException se)
            {
                Trace.WriteLine("There was an error talking to the server: " + se.ToString());
            }

            finally
            {
                Dispose();
            }
        }

        #region Disposable Members
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        private void Dispose(bool disposing)
        {
            if (!_disposed)
            {
                if (disposing)
                {
                    if (_client != null)
                    {
                        _client.Close();
                    }
                }
                _disposed = true;
            }
        }
        #endregion
    }

    class Program
    {
        static void Main()
        {
            MakeClientCallToServer("Just wanted to say hi");
            MakeClientCallToServer("Just wanted to say hi again");
            MakeClientCallToServer("Are you ignoring me?!");

            Console.WriteLine("Press ant key to continue...");
            Console.Read();
        }

        static void MakeClientCallToServer(object objMsg)
        {
            string msg = (string)objMsg;
            MyTcpClient client = new MyTcpClient(IPAddress.Loopback, 55555);
            client.ConnectToServer(msg);
        }
    }
}

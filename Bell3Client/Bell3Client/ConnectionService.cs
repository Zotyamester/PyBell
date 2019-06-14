using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Bell3Client
{
    public class ConnectionService
    {
        private Socket s;
        IPHostEntry hostEntry;
        private Thread thread;
        private volatile bool running = false;
        private Print print;
        private Label label;
        private Print print2;
        private Label label2;

        private const string IP = "127.0.0.1";
        private const int PORT = 55555;

        public ConnectionService(Print print, Label label, Print print2, Label label2)
        {
            thread = new Thread(workerThread);
            this.print = print;
            this.label = label;
            this.print2 = print2;
            this.label2 = label2;

            hostEntry = Dns.GetHostEntry(IP);
            
            foreach (IPAddress address in hostEntry.AddressList)
            {
                IPEndPoint ipe = new IPEndPoint(address, PORT);
                Socket tempSocket =
                    new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

                tempSocket.Connect(ipe);

                if (tempSocket.Connected)
                {
                    s = tempSocket;
                    break;
                }
                else
                {
                    continue;
                }
            }
        }

        private void workerThread()
        {
            try
            {

                {
                    int count = 0;
                    byte[] bytes = new byte[1024];
                    count = s.Receive(bytes, bytes.Length, 0);
                    string msg = Encoding.UTF8.GetString(bytes, 0, count);
                    print2(label2, msg);
                }

                while (running)
                {
                    int count = 0;
                    byte[] bytes = new byte[1024];
                    count = s.Receive(bytes, bytes.Length, 0);
                    string msg = Encoding.UTF8.GetString(bytes, 0, count);
                    print(label, msg);
                    Thread.Sleep(100);
                }
            }
            catch (Exception ex)
            {

            }
        }

        public void Send(string msg)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(msg);
            s.Send(bytes);
        }

        public void Start()
        {
            running = true;
            thread.Start();
        }

        public void Stop()
        {
            running = false;
            thread.Interrupt();
            s.Close();
        }
    }
}

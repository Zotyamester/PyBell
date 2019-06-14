using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using System.Diagnostics;

namespace Bell3Server
{
    public class ConnectionService
    {
        private Socket listener;
        private Socket client;
        public SchedulerService ss;
        private Thread thread;
        private Print print;
        private Label label;
        private PrintOrder printOrder;
        private Label label2;
        private volatile bool running = false;

        public ConnectionService(Print print, Label label, PrintOrder printOrder, Label label2)
        {
            ss = new SchedulerService(print, label);
            this.print = print;
            this.label = label;
            this.printOrder = printOrder;
            this.label2 = label2;
            thread = new Thread(workerThread);
        }

        public void LoadSchedule(string filename)
        {
            ss.ClearSchedule();
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load(filename);
            foreach (XmlNode node in xmlDoc.DocumentElement.ChildNodes)
            {
                string soundname = node.ChildNodes[0].InnerText;
                int[] days = new int[6];
                for (int i = 0; i < 6; i++)
                {
                    days[i] = int.Parse(node.ChildNodes[1].Attributes[i].Value);
                }
                for (int i = 2; i < node.ChildNodes.Count; i++)
                {
                    int hour = int.Parse(node.ChildNodes[i].Attributes[0].Value);
                    int minute = int.Parse(node.ChildNodes[i].Attributes[1].Value);
                    for (int j = 0; j < 6; j++)
                    {
                        if (days[j] == 0)
                            continue;
                        WeekDate date;
                        date.day = j + 1;
                        date.hour = hour;
                        date.minute = minute;
                        ss.ScheduleTask(date, soundname);
                    }
                }
            }
            ss.config = filename;
            ss.PrintSchedule();
            print(label, ss.Closest());
        }

        public void Send(string msg)
        {
            if (client == null)
                return;
            byte[] bytes = Encoding.UTF8.GetBytes(msg);
            client.Send(bytes);
        }

        private void Receive(Socket client)
        {
            int count = 0;
            byte[] bytes = new byte[1024];
            count = client.Receive(bytes, bytes.Length, 0);
            string msg = Encoding.UTF8.GetString(bytes, 0, count);
            LoadSchedule(msg);
            printOrder(label2, msg);
        }

        private void workerThread()
        {
            IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
            IPAddress ipAddress = ipHostInfo.AddressList[0];
            IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 55555);

            // Create a TCP/IP socket.  
            listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            // Bind the socket to the local endpoint and listen for incoming connections.  
            try
            {
                listener.Bind(localEndPoint);
                listener.Listen(100);

                while (running)
                {
                    try
                    {
                        Socket client = listener.Accept();

                        Send(ss.config);

                        while (running && client.Connected)
                        {
                            Receive(client);
                            Thread.Sleep(100);
                        }
                        Thread.Sleep(1000);
                    }
                    catch (Exception ex)
                    {

                    }
                }

            }
            catch (Exception e)
            {

            }
        }

        public void Start()
        {
            ss.Start();
            running = true;
            thread.Start();
        }

        public void Stop()
        {
            running = false;
            thread.Interrupt();
            ss.Stop();
            if (client != null)
                client.Close();
            listener.Close();
        }
    }
}

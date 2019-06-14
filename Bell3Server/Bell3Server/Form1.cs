using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Media;
using System.Xml;
using System.Diagnostics;
using System.IO;
using System.Threading;

namespace Bell3Server
{

    public delegate void Print(Label label, WeekDate date);

    public delegate void PrintOrder(Label label, string text);

    public partial class Form1 : Form
    {


        private ConnectionService cs;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cs = new ConnectionService(PrintNext, lTime, PrintRingOrder, lRing);
            cs.LoadSchedule(@"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
            PrintRingOrder(lRing, @"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
            cs.Start();
        }

        public void PrintRingOrder(Label label, string text)
        {
            if (label.InvokeRequired)
            {
                Invoke(new PrintOrder(PrintRingOrder), label, text);
            }
            else
            {
                lRing.Text = text;
            }
        }
        public void PrintNext(Label label, WeekDate closest)
        {
            if (label.InvokeRequired)
            {
                Invoke(new Print(PrintNext), label, closest);
            }
            else
            {
                string week = "";
                switch (closest.day)
                {
                    case 1:
                        week = "Hétfő";
                        break;
                    case 2:
                        week = "Kedd";
                        break;
                    case 3:
                        week = "Szerda";
                        break;
                    case 4:
                        week = "Csütörtök";
                        break;
                    case 5:
                        week = "Péntek";
                        break;
                    default:
                        week = "Szombat";
                        break;
                }
                lTime.Text = $"{week} {closest.hour}:{closest.minute}";
                cs.Send(lTime.Text);
            }
        }

        private void Form1_FormClosed_1(object sender, FormClosedEventArgs e)
        {
            cs.Stop();
        }
    }
}

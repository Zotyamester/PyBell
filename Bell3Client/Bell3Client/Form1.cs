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

namespace Bell3Client
{

    public delegate void Print(Label label, string text);

    public partial class Form1 : Form
    {
        
        private ConnectionService cs;

        public Form1()
        {
            Thread.CurrentThread.Name = "GUI_Thread";
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cs = new ConnectionService(PrintNext, lTime, PrintOrder, lRing);
            cs.Send(@"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
            cs.Start();
        }

        public void PrintOrder(Label label, string text)
        {
            if (label.InvokeRequired)
            {
                Invoke(new Print(PrintOrder), label, text);
            }
            else
            {
                lRing.Text = text;
            }
        }

        public void PrintNext(Label label, string text)
        {
            if (label.InvokeRequired)
            {
                Invoke(new Print(PrintNext), label, text);
            }
            else
            {
                lTime.Text = text;
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            cs.Send(@"C:\Users\Bethlen\Desktop\Bell\BellConfig-rövid.xml");
            PrintOrder(lRing, @"C:\Users\Bethlen\Desktop\Bell\BellConfig-rövid.xml");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            cs.Send(@"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
            PrintOrder(lRing, @"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            cs.Stop();
        }
        
    }
}

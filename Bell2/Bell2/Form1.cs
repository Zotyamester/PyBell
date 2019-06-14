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

namespace Bell2
{

    public delegate void Print(Label label);

    public partial class Form1 : Form
    {


        private SchedulerService ss;

        public Form1()
        {
            Thread.CurrentThread.Name = "GUI_Thread";
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            ss = new SchedulerService(PrintNext, lTime);
            LoadSchedule(@"C:\Users\Bethlen\Desktop\Bell\BellConfig_normal.xml");
            ss.Start();
        }

        private void LoadSchedule(string filename)
        {
            Debug.WriteLine(filename);
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
            ss.PrintSchedule();
            PrintNext(lTime);
        }

        public void PrintNext(Label label)
        {
            if (label.InvokeRequired)
            {
                Invoke(new Print(PrintNext), label);
            }
            else
            {
                WeekDate closest = ss.Closest();
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
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            LoadSchedule(@"C:\Users\Bethlen\Desktop\Bell\BellConfig-rövid.xml");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            LoadSchedule(@"C:\Users\szatm\Downloads\CSENGŐ\Bell\BellConfig_normal.xml");
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            ss.Stop();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            OpenFileDialog open = new OpenFileDialog();
            if (open.ShowDialog() == DialogResult.OK)
            {
                LoadSchedule(open.FileName);
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Media;
using System.Threading;
using System.Windows.Forms;

namespace Bell3Server
{

    public struct WeekDate
    {
        public int day;
        public int hour;
        public int minute;
    }

    public struct Data
    {
        public WeekDate date;
        public string filename;
    }

    public class SchedulerService
    {

        public string config = "";
        private volatile bool running = false;
        private Thread thread;
        private List<Data> events = new List<Data>();
        private Print print;
        private Label label;
        private SoundPlayer sp = new SoundPlayer();

        public SchedulerService(Print print, Label label)
        {
            thread = new Thread(workerThread);
            this.print = print;
            this.label = label;
        }

        private void workerThread()
        {
            DateTime tm;
            try
            {
                tm = DateTime.Now;
                foreach (Data data in events)
                {
                    if (data.date.day == (int)tm.DayOfWeek && data.date.hour == tm.Hour && data.date.minute == tm.Minute)
                    {
                        PlaySound(data.filename);
                    }
                }
                print(label, Closest());
                Debug.WriteLine((60 - tm.Second)*1000);
                Thread.Sleep((60 - tm.Second) * 1000);
            }
            catch (Exception ex)
            {

            }
            while (running)
            {
                try
                {
                    tm = DateTime.Now;
                    foreach (Data data in events)
                    {
                        if (data.date.day == (int)tm.DayOfWeek && data.date.hour == tm.Hour && data.date.minute == tm.Minute)
                        {
                            PlaySound(data.filename);
                        }
                    }
                    print(label, Closest());
                    Thread.Sleep(60000);
                }
                catch (Exception ex)
                {

                }
            }
        }

        private void PlaySound(string filename)
        {
            sp.Stop();
            sp.SoundLocation = filename;
            sp.Play();
        }

        public void Start()
        {
            thread.Start();
            running = true;
        }

        public void Stop()
        {
            running = false;
            thread.Interrupt();
        }

        public void PrintSchedule()
        {
            foreach (Data data in events)
            {
                Debug.WriteLine($"Day - {data.date.day} - {data.date.hour}:{data.date.minute}");
            }
        }

        private int Cmp(WeekDate d1, WeekDate d2)
        {
            if (d1.day < d2.day)
                return -1;
            if (d1.day > d2.day)
                return 1;
            if (d1.hour < d2.hour)
                return -1;
            if (d1.hour > d2.hour)
                return 1;
            if (d1.minute < d2.minute)
                return -1;
            if (d1.minute > d2.minute)
                return 1;
            return 0;
        }

        private int Dcmp(Data d1, Data d2)
        {
            return Cmp(d1.date, d2.date);
        }

        private void Sort()
        {
            events.Sort(Dcmp);
        }

        public WeekDate Closest()
        {
            DateTime tm = DateTime.Now;
            WeekDate now;
            now.day = ((int)tm.DayOfWeek == 0) ? 7:(int)tm.DayOfWeek;
            now.hour = tm.Hour;
            now.minute = tm.Minute;
            int i;
            for (i = 0; i < events.Count && Cmp(events[i].date, now) == -1; i++);
            return events[i].date;
        }

        public void ClearSchedule()
        {
            events.Clear();
        }
        
        public void ScheduleTask(WeekDate date, string filename)
        {
            Data data;
            data.date = date;
            data.filename = filename;
            events.Add(data);
            Sort();
            thread.Interrupt();
        }
    }
}
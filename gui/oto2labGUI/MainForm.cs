using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace oto2labGUI
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }
        #region file path D&D
        private void TextBox_DragEnter(object sender, DragEventArgs e)
        {
            e.Effect = DragDropEffects.All;
        }

        private void TextBox_DragDrop(object sender, DragEventArgs e)
        {
            if (!e.Data.GetDataPresent(DataFormats.FileDrop)) return;
            string[] learnFile = (string[])e.Data.GetData(DataFormats.FileDrop);
            TextBox textBox = (TextBox)sender;
            textBox.Text = learnFile[0];
        }


        #endregion

        private void InputFilePath_textBox_TextChanged(object sender, EventArgs e)
        {
            ExecuteButtonEnableCheck();
        }

        private void FileBrowse_button_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "File(*.*)|*.*";
            ofd.Title = "File Select";
            ofd.RestoreDirectory = true;
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                InputPath_textBox.Text = ofd.FileName;
            }
        }
        private void FolderBrowse_button_Click(object sender, EventArgs e)
        {
            //FolderBrowserDialog fbd = new FolderBrowserDialog();
            //fbd.Description = "Folder select";
            //if (fbd.ShowDialog(this) == DialogResult.OK)
            //{
            //    InputPath_textBox.Text = fbd.SelectedPath;
            //}
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "Folder(.)|.";
            ofd.Title = "Folder Select";
            ofd.FileName = "SelectFolder";
            ofd.CheckFileExists = false;
            ofd.RestoreDirectory = true;
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                InputPath_textBox.Text = System.IO.Path.GetDirectoryName(ofd.FileName);
            }
        }

        private void ExecuteButtonEnableCheck()
        {
            if(InputPath_textBox.Text != "" )
            {
                Execute_button.Enabled = true;
            }
            else
            {
                Execute_button.Enabled = false;
            }
        }

        private void Execute_button_Click(object sender, EventArgs e)
        {
            // fix string
            string fixStr = " --gui";
            // input file
            string inputFileStr = " --input " + InputPath_textBox.Text;

            // set option string
            string optionStr = " --mode ";
            var RadioButtonChecked_InGroup = Option_groupBox.Controls.OfType<RadioButton>().SingleOrDefault(rb => rb.Checked == true);
            switch (RadioButtonChecked_InGroup.Name)
            {
                case "ustToOto_radioButton":
                    optionStr += "1";
                    break;
                case "otoToLab_radioButton":
                    optionStr += "2";
                    break;
                case "labToOto_radioButton":
                    optionStr += "3";
                    break;
                case "svpToOto_radioButton":
                    optionStr += "4";
                    break;
            }

            // set option of mode
            /*
            if(debugMode_checkBox.Checked == true)
            {
                optionStr += " --debug";
            }
            */
            if(KanaAlias_checkBox.Checked == true)
            {
                optionStr += " --kana";
            }


            // make process
            ProcessStartInfo psInfo = new ProcessStartInfo();
            psInfo.FileName = "oto2lab.exe";
            psInfo.CreateNoWindow = true;
            psInfo.UseShellExecute = false;
            psInfo.RedirectStandardOutput = true;
            psInfo.Arguments = inputFileStr + optionStr + fixStr;

            // execute exe file with option
            Process ps = Process.Start(psInfo);
            ps.WaitForExit();

            // output return string
            if (ps.ExitCode != 0)
            {   string output = ps.StandardOutput.ReadToEnd();
                output = output.Replace("\r\r\n", "\n");
                standardOut_textBox.Text = "error occured from oto2lab.exe\n" + output;
            }
            else
            {
                string output = ps.StandardOutput.ReadToEnd();
                output = output.Replace("\r\r\n", "\n");
                standardOut_textBox.Text = output;
            }
        }
    }
}

namespace oto2labGUI
{
    partial class MainForm
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.InputPath_textBox = new System.Windows.Forms.TextBox();
            this.InputPath_label = new System.Windows.Forms.Label();
            this.Option_groupBox = new System.Windows.Forms.GroupBox();
            this.svpToOto_radioButton = new System.Windows.Forms.RadioButton();
            this.labToOto_radioButton = new System.Windows.Forms.RadioButton();
            this.otoToLab_radioButton = new System.Windows.Forms.RadioButton();
            this.ustToOto_radioButton = new System.Windows.Forms.RadioButton();
            this.Execute_button = new System.Windows.Forms.Button();
            this.FileBrowse_button = new System.Windows.Forms.Button();
            this.standardOut_textBox = new System.Windows.Forms.TextBox();
            this.standardOut_label = new System.Windows.Forms.Label();
            this.FolderBrowse_button = new System.Windows.Forms.Button();
            this.appendOption_groupBox = new System.Windows.Forms.GroupBox();
            this.KanaAlias_checkBox = new System.Windows.Forms.CheckBox();
            this.Option_groupBox.SuspendLayout();
            this.appendOption_groupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // InputPath_textBox
            // 
            this.InputPath_textBox.AllowDrop = true;
            this.InputPath_textBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.InputPath_textBox.Location = new System.Drawing.Point(121, 12);
            this.InputPath_textBox.Name = "InputPath_textBox";
            this.InputPath_textBox.ReadOnly = true;
            this.InputPath_textBox.Size = new System.Drawing.Size(465, 19);
            this.InputPath_textBox.TabIndex = 1;
            this.InputPath_textBox.TextChanged += new System.EventHandler(this.InputFilePath_textBox_TextChanged);
            this.InputPath_textBox.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.InputPath_textBox.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // InputPath_label
            // 
            this.InputPath_label.AutoSize = true;
            this.InputPath_label.Location = new System.Drawing.Point(12, 15);
            this.InputPath_label.Name = "InputPath_label";
            this.InputPath_label.Size = new System.Drawing.Size(103, 12);
            this.InputPath_label.TabIndex = 0;
            this.InputPath_label.Text = "Input File or Folder";
            // 
            // Option_groupBox
            // 
            this.Option_groupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Option_groupBox.Controls.Add(this.svpToOto_radioButton);
            this.Option_groupBox.Controls.Add(this.labToOto_radioButton);
            this.Option_groupBox.Controls.Add(this.otoToLab_radioButton);
            this.Option_groupBox.Controls.Add(this.ustToOto_radioButton);
            this.Option_groupBox.Location = new System.Drawing.Point(12, 39);
            this.Option_groupBox.Name = "Option_groupBox";
            this.Option_groupBox.Size = new System.Drawing.Size(776, 48);
            this.Option_groupBox.TabIndex = 4;
            this.Option_groupBox.TabStop = false;
            this.Option_groupBox.Text = "Option";
            // 
            // svpToOto_radioButton
            // 
            this.svpToOto_radioButton.AutoSize = true;
            this.svpToOto_radioButton.Location = new System.Drawing.Point(242, 18);
            this.svpToOto_radioButton.Name = "svpToOto_radioButton";
            this.svpToOto_radioButton.Size = new System.Drawing.Size(75, 16);
            this.svpToOto_radioButton.TabIndex = 2;
            this.svpToOto_radioButton.Text = "svp to oto";
            this.svpToOto_radioButton.UseVisualStyleBackColor = true;
            // 
            // labToOto_radioButton
            // 
            this.labToOto_radioButton.AutoSize = true;
            this.labToOto_radioButton.Location = new System.Drawing.Point(164, 18);
            this.labToOto_radioButton.Name = "labToOto_radioButton";
            this.labToOto_radioButton.Size = new System.Drawing.Size(72, 16);
            this.labToOto_radioButton.TabIndex = 2;
            this.labToOto_radioButton.Text = "lab to oto";
            this.labToOto_radioButton.UseVisualStyleBackColor = true;
            // 
            // otoToLab_radioButton
            // 
            this.otoToLab_radioButton.AutoSize = true;
            this.otoToLab_radioButton.Location = new System.Drawing.Point(86, 18);
            this.otoToLab_radioButton.Name = "otoToLab_radioButton";
            this.otoToLab_radioButton.Size = new System.Drawing.Size(72, 16);
            this.otoToLab_radioButton.TabIndex = 1;
            this.otoToLab_radioButton.Text = "oto to lab";
            this.otoToLab_radioButton.UseVisualStyleBackColor = true;
            // 
            // ustToOto_radioButton
            // 
            this.ustToOto_radioButton.AutoSize = true;
            this.ustToOto_radioButton.Checked = true;
            this.ustToOto_radioButton.Location = new System.Drawing.Point(7, 19);
            this.ustToOto_radioButton.Name = "ustToOto_radioButton";
            this.ustToOto_radioButton.Size = new System.Drawing.Size(73, 16);
            this.ustToOto_radioButton.TabIndex = 0;
            this.ustToOto_radioButton.TabStop = true;
            this.ustToOto_radioButton.Text = "ust to oto";
            this.ustToOto_radioButton.UseVisualStyleBackColor = true;
            // 
            // Execute_button
            // 
            this.Execute_button.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.Execute_button.Enabled = false;
            this.Execute_button.Location = new System.Drawing.Point(715, 147);
            this.Execute_button.Name = "Execute_button";
            this.Execute_button.Size = new System.Drawing.Size(75, 23);
            this.Execute_button.TabIndex = 6;
            this.Execute_button.Text = "Execute";
            this.Execute_button.UseVisualStyleBackColor = true;
            this.Execute_button.Click += new System.EventHandler(this.Execute_button_Click);
            // 
            // FileBrowse_button
            // 
            this.FileBrowse_button.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.FileBrowse_button.Location = new System.Drawing.Point(592, 10);
            this.FileBrowse_button.Name = "FileBrowse_button";
            this.FileBrowse_button.Size = new System.Drawing.Size(85, 23);
            this.FileBrowse_button.TabIndex = 2;
            this.FileBrowse_button.Text = "File Browse";
            this.FileBrowse_button.UseVisualStyleBackColor = true;
            this.FileBrowse_button.Click += new System.EventHandler(this.FileBrowse_button_Click);
            // 
            // standardOut_textBox
            // 
            this.standardOut_textBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.standardOut_textBox.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.standardOut_textBox.ForeColor = System.Drawing.SystemColors.Window;
            this.standardOut_textBox.Location = new System.Drawing.Point(14, 176);
            this.standardOut_textBox.Multiline = true;
            this.standardOut_textBox.Name = "standardOut_textBox";
            this.standardOut_textBox.ReadOnly = true;
            this.standardOut_textBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.standardOut_textBox.Size = new System.Drawing.Size(776, 95);
            this.standardOut_textBox.TabIndex = 7;
            // 
            // standardOut_label
            // 
            this.standardOut_label.AutoSize = true;
            this.standardOut_label.Location = new System.Drawing.Point(17, 161);
            this.standardOut_label.Name = "standardOut_label";
            this.standardOut_label.Size = new System.Drawing.Size(176, 12);
            this.standardOut_label.TabIndex = 5;
            this.standardOut_label.Text = "Standard Output from oto2lab.exe";
            // 
            // FolderBrowse_button
            // 
            this.FolderBrowse_button.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.FolderBrowse_button.Location = new System.Drawing.Point(683, 10);
            this.FolderBrowse_button.Name = "FolderBrowse_button";
            this.FolderBrowse_button.Size = new System.Drawing.Size(105, 23);
            this.FolderBrowse_button.TabIndex = 3;
            this.FolderBrowse_button.Text = "Folder Browse";
            this.FolderBrowse_button.UseVisualStyleBackColor = true;
            this.FolderBrowse_button.Click += new System.EventHandler(this.FolderBrowse_button_Click);
            // 
            // appendOption_groupBox
            // 
            this.appendOption_groupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.appendOption_groupBox.Controls.Add(this.KanaAlias_checkBox);
            this.appendOption_groupBox.Location = new System.Drawing.Point(14, 93);
            this.appendOption_groupBox.Name = "appendOption_groupBox";
            this.appendOption_groupBox.Size = new System.Drawing.Size(776, 48);
            this.appendOption_groupBox.TabIndex = 4;
            this.appendOption_groupBox.TabStop = false;
            this.appendOption_groupBox.Text = "Append option";
            // 
            // KanaAlias_checkBox
            // 
            this.KanaAlias_checkBox.AutoSize = true;
            this.KanaAlias_checkBox.Location = new System.Drawing.Point(5, 18);
            this.KanaAlias_checkBox.Name = "KanaAlias_checkBox";
            this.KanaAlias_checkBox.Size = new System.Drawing.Size(79, 16);
            this.KanaAlias_checkBox.TabIndex = 8;
            this.KanaAlias_checkBox.Text = "Kana Alias";
            this.KanaAlias_checkBox.UseVisualStyleBackColor = true;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 284);
            this.Controls.Add(this.standardOut_label);
            this.Controls.Add(this.standardOut_textBox);
            this.Controls.Add(this.FolderBrowse_button);
            this.Controls.Add(this.FileBrowse_button);
            this.Controls.Add(this.Execute_button);
            this.Controls.Add(this.appendOption_groupBox);
            this.Controls.Add(this.Option_groupBox);
            this.Controls.Add(this.InputPath_label);
            this.Controls.Add(this.InputPath_textBox);
            this.MaximizeBox = false;
            this.MinimumSize = new System.Drawing.Size(816, 323);
            this.Name = "MainForm";
            this.Text = "oto2labGUI";
            this.Option_groupBox.ResumeLayout(false);
            this.Option_groupBox.PerformLayout();
            this.appendOption_groupBox.ResumeLayout(false);
            this.appendOption_groupBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox InputPath_textBox;
        private System.Windows.Forms.Label InputPath_label;
        private System.Windows.Forms.GroupBox Option_groupBox;
        private System.Windows.Forms.Button Execute_button;
        private System.Windows.Forms.Button FileBrowse_button;
        private System.Windows.Forms.RadioButton labToOto_radioButton;
        private System.Windows.Forms.RadioButton otoToLab_radioButton;
        private System.Windows.Forms.RadioButton ustToOto_radioButton;
        private System.Windows.Forms.TextBox standardOut_textBox;
        private System.Windows.Forms.Label standardOut_label;
        private System.Windows.Forms.Button FolderBrowse_button;
        private System.Windows.Forms.RadioButton svpToOto_radioButton;
        private System.Windows.Forms.GroupBox appendOption_groupBox;
        private System.Windows.Forms.CheckBox KanaAlias_checkBox;
    }
}


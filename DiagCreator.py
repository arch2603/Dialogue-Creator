#!/usr/bin/python

from subprocess import Popen, PIPE
from Tkinter import *
#from Tkinter import ttk
from tkFileDialog import askopenfile

import tkFileDialog
import string
import wave
import tkMessageBox
#import ImageTk
import os,sys

#images used for emotional settings
imagehappy = 'images/happysmall.gif/'
imagesad = 'images/sadface.gif/'
imagerecord = 'images/record.gif/'

#File options available to the user when when selecting Find Directory Option
FILEOPTIONS = dict(defaultextension='.scm', filetypes=[('Bin File','*.wav'),('ALL files','*.*')])

class Application:
    
    '''
        Method: _init_(intialisation)
        Type: Instance
        Parameter: self, master
        Description: The init method is the main constructor which initialised the GUI widgets by passing in a frame widget that will be used
        to create the main UI buttons and other widgets  
    '''   
    def __init__(self, master): #This method initializes and creates the application
           
        self.master = master
                             
        frame = Frame(master)
        frame.pack()
            
        self.createGUI(frame, master) #creating the GUI
    
    '''
        Method: createGUI
        Type: Instance
        Parameter: self,frame, master
        Description: The method is responsible for creating all the GUI widgets appear on the UI such as buttons, frames, top-level widgets etc
    '''      
   
    def createGUI(self, frame, master):#This method creates the GUI, there are 4 main frames.
        
        #Defining options for opening a directory
        self.dir_opt = options ={}
        options['initialdir'] = '/home/../Documents'
        options['mustexist'] = False
        options['parent']= root
        options['title'] = 'Find Directory'
                        
              
        '''
        The following section groups buttons and another widgets that are in the same frame such as 
        play, Pause, Continue and Delete Text
        '''
        
        #TEXT BOX FRAME (contains the text area, play button and save audio file button0
              
        txtBoxFrame = Frame(frame, bd=1, relief=RAISED)
        txtBoxFrame.grid(row=0, column=0, rowspan=4, sticky = N)
        
        self.txtBoxLabel = Label(txtBoxFrame, text="Enter Text For Speech:")#label for the text box
        self.txtBoxLabel.grid(row=0, )
                
        self.txtBox = Text(txtBoxFrame, height=14, width=50, wrap=WORD)
        self.txtBox.grid(row=1)
        
        #Creating a scrollbar inside the text widget
        self.vscrollbar = Scrollbar(txtBoxFrame, orient = VERTICAL)
   
#        self.txtBox.grid(row=2)
        self.txtBox.config(yscrollcommand = self.vscrollbar.set)
        self.vscrollbar.grid(row = 1, column = 1, sticky=N+E)
        self.vscrollbar.configure(command = self.txtBox.yview)
        
        
        #Creating frame to house play button, Pause and Continue
        play_cont_play_frame = Frame(frame, bd=1, relief = RAISED)
        play_cont_play_frame.grid(row=0,column = 1, rowspan=4, sticky =N)
        
        #Play Button
        self.btn_Speak = Button(play_cont_play_frame, text="Play Back", 
                                command=lambda: self.speak(self.txtBox.get(1.0, END), voice), width=20, height=5,fg="green")
        self.btn_Speak.grid(row=0, column=0, sticky=N)
        
        #Pause Button         
        self.btn_pause = Button(play_cont_play_frame, text = "Pause",command=self.pause_talk,width=20, height=5)
        self.btn_pause.grid(row=0, column=1, sticky=N)
        
        #Continue Button        
        self.btn_cont = Button(play_cont_play_frame, text = "Continue",command=self.cont_talk,width= 43,height=4)
        self.btn_cont.grid(row=1, column=0,columnspan = 4, sticky=W+E+N+S)
        
        #Clear text box writing
        self.btn_cleartxt = Button( play_cont_play_frame, text="Clear Text Box", 
                                     command=lambda: self.deleteText(), width=43, height=4)
        self.btn_cleartxt.grid(row=2, column=0,columnspan = 4, sticky=W+E+N+S)
        
#*******************************************************************************************************************************

        '''
            This following statements creates a frame for Hear
        '''
        #Creating frame for saving text to audio file button
        
        frameMisc = Frame(frame, bd = 1, relief = SUNKEN, width=50)
        frameMisc.grid(row=4,column=0, columnspan=100,sticky=N+S+W+E)
        
        self.btn_txt2wave = Button(frameMisc, text="Save Text As Audio File", 
                                   command=lambda: self.txt2wave(voice),width=28,height=2,bd=2)
        self.btn_txt2wave.grid(row=0, column=0,sticky=W+E+N+S,padx=1,pady=1) 
      
        
        #Save scm commands button
        
        self.btn_SaveCommands = Button( frameMisc, text="Save Commands", 
                                        command=lambda: self.saveCommands(voice),width=27, height=2,bd=2)
        self.btn_SaveCommands.grid(row=0, column=1, sticky=W+E+N+S,padx=1,pady=1)
        
        #Delete text box writing
        self.btn_cleartxt = Button( frameMisc, text="Delete Text", 
                                     command=lambda: self.deleteText(), width=27, height=2,bd=2)
        self.btn_cleartxt.grid(row=0, column=2,sticky=W+E+N+S,padx=1,pady=1)
        
        
        #RECORDING FRAME (contains button to go to the recording section)
        
        #this button takes the user to the recording section of the app
        
        self.imagerecord = PhotoImage(file = imagerecord )
        
        self.btn_recordVoice = Button(frameMisc, text="Voice Recording",
                                      command=lambda: self.switchingToRecord(frame, master), width=720, height=30)
        self.btn_recordVoice.grid_propagate(False)
        self.btn_recordVoice.config(image=self.imagerecord, compound=LEFT)
        self.btn_recordVoice.grid(row=2, column=0, rowspan=100,columnspan=100)
        
        
        
        '''
        This statement creates the frame and buttons for emotional 
        '''
        #Frame and Button for browsing a File
        file_locate = Frame(frame, bd=1, relief=FLAT, width=25)
        file_locate.grid(row=6,column=0, sticky=N,columnspan=100,rowspan=100)
        self.btn_gotoFile = Button(file_locate, text="Find Directory", width=90, height=1, command=lambda: self.defaultFileLocation())
        self.btn_gotoFile.grid(row=0, column=0, sticky=W)
        
        #Creatin images for Happy Emotion
        self.imagehappy = PhotoImage(file = imagehappy )
        self.imagesad = PhotoImage(file = imagesad )
        
        emoFrame = Frame(frame, bd=1, relief=FLAT, width=25)
        emoFrame.grid(row=8,column=0, sticky=S,columnspan=100,rowspan=100)
        
        #Creating Label for Settings and Emotions
        self.settingslabel = Label(file_locate,  text = "Settings", relief = RAISED, font = ("Times New Roman", 20, "bold"),fg="blue",bg="white")

        self.settingslabel.grid(row=2, column=0, sticky=N+S+W+E)
        
        self.emotionallabel = Label(file_locate, text="Emotions:", font=("20"), height=3)
        self.emotionallabel.grid(row =4, column = 0, sticky=W+E)
    
        
        #Creating different emotional buttons
        
        self.btn_happy = Button(file_locate, text = "Happy!!", image = self.imagehappy,compound= RIGHT,font=("Arial", "12"),width=350,height=55, 
                                fg= "green",bg="yellow", highlightcolor = "yellow",highlightbackground="yellow",command=lambda:self.sayemotional(self.speak(self.message, voice)))
        self.btn_happy.configure(relief= RAISED)
        self.btn_happy.grid(row = 6, column = 0, sticky = W,ipadx=2, ipady=2)
        
        self.btn_neutral = Button(file_locate, text = "Neutral", bg = "lightblue",font = ("Arial", "12"), fg="black", width=37, height=3)
        self.btn_neutral.configure(relief= RAISED)
        self.btn_neutral.grid(row = 6, column = 0 , sticky =E, ipadx=2, ipady=1)
        
         
 
        '''
        The statements below established a frame which contains a scale and other widgets such as radio buttons for different voices
        '''
        #VOICE FRAME(contains the available voices list)
        misc_frame = Frame(frame, bd=1, relief=FLAT)#positioning voiceFrame within the main frame
        misc_frame.grid(row=200, column=0,columnspan=100)
        
        misc_frame2 = Frame(frame, bd=1, relief=FLAT)
        misc_frame2.grid(row=202, column=0,columnspan=100)
        
        #Slider Scale for rate of speech and Label:
        self.rateofspeechlabel = Label(misc_frame, text="Rate of Speech:", font=("20"), height=2)
        self.rateofspeechlabel.grid(row =0, column = 0, sticky=W+E)
        
        self.sld_slider = Scale(misc_frame, from_=1, to=10, orient= HORIZONTAL, width=30, length=500)
        self.sld_slider.grid(row=1, column=0, sticky=N+W)
        self.sld_slider.configure(tickinterval =0.0)
        
               
        #Label for Available voices        
        self.voicesLabel = Label(misc_frame2, text="Avaliable Voices:", font=("20"))#label for the frame
        self.voicesLabel.grid(row=0,sticky=W+E)
        
        #Different accents i.e.NZ and USA using radio button        
        voice = IntVar()#radio buttons to select voices
        rbNZE = Radiobutton(misc_frame2, text="New Zealand Voice", variable=voice, value=1)
        rbKAL = Radiobutton(misc_frame2, text="American Voice", variable=voice, value=2)
        rbNZE.grid(row=1,column=0, sticky=W+E+N+S)
        rbKAL.grid(row=1, column=1,sticky= W+E+N+S)       
       


        '''
        This statement changes the color of the emotional label depending on which button is pressed
        '''        
        '''
        ---------------------------------------------------------------------------------------
        ''' 
        
                     
    '''
        Method: pause_talk
        Type: Instance
        Parameter: self
        Description: The pause_talk method handles the pausing of the speech while
        festival is speaking
    '''   
    def pause_talk(self):
        
        command = "killall -STOP aplay "
#        
        result, errors = Popen(command, shell=True, stdout=PIPE ).communicate()
        
      
    '''
        Method: cont_talk
        Type: Instance
        Parameter: self
        Description: The cont_talk is the continue talk method which stops the process
        or festival from speaking when the use pause the speech. Note the speech starts
        from where it was paused
        
    '''   
    def cont_talk(self):
        
        command = "killall -CONT aplay "
        result, errors = Popen(command, shell=True, stdout=PIPE ).communicate()
        
      
        
        
    '''
    This following statements creates a frame for Recording
    '''    
    def emotionalcolorchange(self): 
        
        if self.btn_happy["background"] == "yellow":
            self.emotionallabel["background"] = "yellow"
    '''
    ---------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------
    '''      
            
#        self.btn_happy.configure()

    '''
        Method: speak
        Type: Instance
        Parameter: self, message, voice
        Description: The speak method acquires the message and voice and speaks the message base on the accent passed in
        
    '''   
    def speak(self, message, voice):#This method is used to speak the text in the text box in the selected voice
        
        if len(message.split(' ')) > 30:#spliting the text by '.' if there are more than 30 words
            splitMessage = string.split(message, '.')
            
            for i in range (len(splitMessage)):  
                if voice.get() == 1:#if current selecting is NZE voice
                   Popen(['/usr/bin/festival', '-b', '(voice_akl_nz_jdt_diphone)', '(SayText "'+splitMessage[i]+'")']).wait()
                    
                    
                else:#default
                   Popen(['/usr/bin/festival', '-b', '(voice_kal_diphone)', '(SayText "'+splitMessage[i]+'")']).wait()
                    
            return splitMessage
                                    
        else:#if string is less than 30 words
            if voice.get() == 1:   
                Popen(['/usr/bin/festival', '-b', '(voice_akl_nz_jdt_diphone)', '(SayText "'+message+'")'])
                
            
            else:
                Popen(['/usr/bin/festival', '-b', '(voice_kal_diphone)', '(SayText "'+message+'")'])
            
            return message           
    
    '''
        Method: sayEmotional
        Type: Instance
        Parameter: self, 
        Description: The speak method acquires the message and voice and speaks the message base on the accent passed in
        
    '''     
    
    def sayemotional(self, msg): 
        
#        if voice.get()== 1:
#            msg = self.speak(message, voice)
            Popen(['/usr/bin/festival', '-b',  '(SayEmotional \'Happy "'+msg+'" 3)'])
#     Popen(['/usr/bin/festival', '-b', '(voice_kal_diphone)', '(SayEmotional \'Happy "'+msg+'" 3)'])
    
    
    '''
        Method: speed
        Type: Instance
        Parameter: self, message, voice
        Description: The speak method acquires the message and voice and speaks the message base on the accent passed in
        
    '''     
    
    def speed(self, msg): 
        
#        if voice.get()== 1:
#            msg = self.speak(message, voice)
            Popen(['/usr/bin/festival', '-b',  '(SayEmotional \'Happy "'+msg+'" 3)'])

    
    
    '''
        Method: Delete Text(deleteText)
        Parameter: self
        Description: Delete or clear the text in the text window or widget
    '''
    
        
    def deleteText(self):#This method to delete what is currently in the text box
        self.txtBox.delete(1.0, END)

    '''
        Method: Text To Wave(txt2wave)
        Parameter: self
        Description: Converts the text file into a wave file
    '''
    
    def txt2wave(self, voice):#This method converts what's in the text box to a .wav file
        
        wavFileName = tkFileDialog.asksaveasfilename(title="Save As")#asking for a save file name and location
        
        txtProcess = Popen("echo "+self.txtBox.get(1.0, END), shell=True, stdout=PIPE)
        
        if voice.get() == 1:#checking what voice is currently selected
            Popen("text2wave -o "+wavFileName+'.wav -eval "(voice_akl_nz_jdt_diphone)"', shell=True, stdin=txtProcess.stdout)
        else:
            Popen("text2wave -o "+wavFileName+'.wav -eval "(voice_kal_diphone)"', shell=True, stdin=txtProcess.stdout)
    
    '''
        Method: saveCommands
        Parameter: self, voice
        Description: Save commands gets invoke by the save command button and allow the button via calling this method
        to save commands such as text on the GUI screen and the two different voices i.e. NZ and USA. 
             
    '''    
    
    def saveCommands(self, voice):#This method saves the current text and voice selection as a .scm file
        
        scmCommandFileName = tkFileDialog.asksaveasfilename(title="Save As")#asking for save name
        
        saveFile = open(scmCommandFileName+".scm", "w")#creating the file
        
        if voice.get() == 1:
            saveFile.write('(voice_akl_nz_jdt_diphone)\n')
        else:
            saveFile.write('(voice_kal_diphone)\n')
        saveFile.write('(SayText "'+self.txtBox.get(1.0, END)[0:-1]+'")\n') 
        
#        return saveFile   
            
    
    '''
        Method: voiceRecord
        Parameter: self
        Description: This methods is called from the recording button and then depending on the users response to a
        yes/no response the recoding will either start or get cancel. It will also ask the user browse where to save
        the recordings and whether the user needs to hear the recording back      
    '''
    def voiceRecord(self):#This method deals with all the recording of user speech
         
        #starting the recording        
        Popen("arecord -r 16000 -t wav unsavedRecording.wav", shell=True)
        
        #telling user to click ok when they are done recoring
        tkMessageBox.askokcancel("Recording Your Voice Now",
                                               "Your Voice Is Now Being Recorded Click OK To Stop Recording")
        Popen("killall arecord", shell=True)#killing the recording process no matter what
        
            
        #asking if user wants to save recording
        saveRecord = tkMessageBox.askyesno("Save Recording", "Do you want to save that recording?")
            
        if saveRecord == True:#saving recording if users says yes
                
            global saveName 
            saveName = tkFileDialog.asksaveasfilename(title="Save As")
            Popen('mv "unsavedRecording.wav" '+str(saveName)+'.wav', shell=True)
                
            #asking user if they want to replay what they just recorded
            replay = tkMessageBox.askyesno("Replay Recording", "Do you want to hear your recording?")
                
            if replay == True:
                self.replayRecording()
    
    '''
        Method: replayRecording
        Parameter: self
        Description:       
    '''
    
    
    def replayRecording(self):#This method deals with replaying user recordings
        
        #try/catch statement to stop users from replaying recording before they have recorded anything
        try:
            Popen("aplay "+saveName+".wav", shell=True)#playing recording
            
        except NameError:
            tkMessageBox.askokcancel("Error","Record Something And Save It First!")
    
    '''
        Method: switchToRecord
        Parameter: self, frame, master
        Description:       
    '''          
    
    
    def switchingToRecord(self, frame, master):#This method sets up the recording GUI
        
        #positioning the GUI where the old window used to be
        x = frame.winfo_rootx()
        y = frame.winfo_rooty()
        
        #hiding main window
        master.withdraw()
        
        #creating new GUI
        self.createRecordingGUI(x, y, master)
    
    '''
        Method: createRecordingGUI
        Parameter: self, x,y, master
        Description: This method creates the buttons are toplevel widget i.e. creating window on top of other windows      
    '''            
    def createRecordingGUI(self, x, y, master):#This method creates the recording GUI to access the recording features
        
        #new frame
        rframe = Toplevel()
        rframe.geometry("%+d%+d" % (x, y))#geometry from previous frame
        rframe.title("Recording")  
        
        #button to start recording
        self.btn_voiceRec = Button(rframe, text="Record Your Voice",
                                    command=lambda: self.voiceRecord(), width=30, height=4)
        self.btn_voiceRec.grid(row=0, column=0)
        
        #button to replay the last recording
        self.btn_voiceRec2 = Button(rframe, text="Replay Last Recording",
                                     command=lambda: self.replayRecording(), width=30, height=4)
        self.btn_voiceRec2.grid(row=0, column=1)
        
        #button to go back to the text synthesis screen
        self.btn_close = Button(rframe, text="Go Back Main Screen",
                                 command=lambda: self.goBack(master, rframe), width=60, height=4)
        self.btn_close.grid(row=1, column=0, columnspan=4, ipadx=14)
    
    '''
        Method: goBack
        Parameter: self, frame, master
        Description:       
    '''    
    def goBack(self, master, frame):#This method is used to go back to the text synthesis screen from the recording one
        master.deiconify()#unhiding the master frame
        frame.destroy()#destroying the createRecordingGUI frame
        
    '''
        Method: defaultFileLocation
        Parameter: self
        Description:       
    '''
    def defaultFileLocation(self):
        return tkFileDialog.askdirectory(**self.dir_opt)
   
                     
root = Tk()
root.title("Dialogue Creator")

#positioning the master frame in approximately the center of the screen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x = (width/2) - 250
y = (height/2) - 250
root.geometry("%+d%+d" % (x, y))

app = Application(root)
root.mainloop()

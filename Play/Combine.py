from tkinter import *
from pytube import YouTube
from pytube import Playlist
from PIL import Image,ImageTk
from moviepy.video.io.VideoFileClip import VideoFileClip
from youtubesearchpython import SearchVideos
import json
import requests
import os
import time
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
import re
######
# Youtube的api key: AIzaSyDmwM77hcEW0XgPg-NUJAgpCjxMJ8PLpf4
from moviepy.editor import AudioFileClip
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter.filedialog import askdirectory
import tkinter as tk  
import pygame
import random
import io
import threading

road=os.path.abspath(__file__).split('Combine.py')[0]
music_location=road+'/music/'
picture_location=road+'/picture/'
url='' #讀取到的網址
p=0 #進度條的標籤
i=0 #歌曲的標籤
pause = False #是否暫停
jumping=False #是否正在換歌
running = True #是否執行自動播放
loop=False #是否執行循環功能
reset=False #換歌後的播放條重置
stop_time=0 #暫停時的當前播放時間
musicList = os.listdir(music_location) #取得音樂
no_Image=False
a,b,c=1,2,3
main_bg=road+'/background_gif/background3.gif'
dl_bg=road+'/background_gif/background3.gif'
music_bg=road+'/background_gif/background3.gif'

print(os.getcwd())

def download_window():
    window = Tk()
    window.geometry("1000x580")
    window.resizable(0,0)

    #使用者要不要下載整個清單的布林值
    chVar_List=BooleanVar()
    #使用者要不要下載圖片的布林值
    chVar_Image=BooleanVar()


    '''
    # 設定背景「圖片」
    temp=Image.open(road+'/background_jpg'+'background8.jpg') 
    # temp=im=size_set(temp)
    temp=temp.resize((1000, 580), Image.ANTIALIAS)
    bg_image=ImageTk.PhotoImage(temp)

    background_label = tk.Label(window,image=bg_image)

    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    '''


    class MyLabel(Label):
        def __init__(self, master, filename):
            im = Image.open(filename)
            seq =  []
            try:
                while 1:
                    seq.append(im.copy())
                    im.seek(len(seq)) # skip to next frame
            except EOFError:
                pass # we're done

            try:
                self.delay = im.info['duration']
            except KeyError:
                self.delay = 100

            first = seq[0].convert('RGBA')
            self.frames = [ImageTk.PhotoImage(first)]

            Label.__init__(self, master, image=self.frames[0])

            temp = seq[0]
            for image in seq[1:]:
                temp.paste(image)
                frame = temp.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))

            self.idx = 0

            self.cancel = self.after(self.delay, self.play)

        def play(self):
            self.config(image=self.frames[self.idx])
            self.idx += 1
            if self.idx == len(self.frames):
                self.idx = 0
            self.cancel = self.after(self.delay, self.play)        



    anim = MyLabel(window, dl_bg)
    anim.place(x=0, y=0, relwidth=1, relheight=1)







    # 第4步，在圖形介面上設定標籤

    l = Label(window,text='Download',bg='black', fg='white', font=('Arial', 18), width=40, height=2)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    l.grid(row=0,column=0,columnspan=2)

    title = Label(window,text='',bg='black', fg='white', font=('Arial', 18), width=30, height=2)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    title.grid(row=4,column=0,columnspan=2)

    textExample=Text(window, height=4,width=60)
    textExample.grid(row=1,column=0,columnspan=2,pady=(10,0))


    #設計圖片

    imLabel=Label(window)
    imLabel.grid(row=3,column=0,columnspan=2,pady=(20,0))


    def long_set(l):        #所有的中文,日文,韓文
        jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3\u4e00-\u9fa5]')  # \uAC00-\uD7A3為匹配韩文的，其餘為日文
        if jap.search(l):
            if(len(l)>20):
                return l[0:20]+'...'
            else:
                return l
        else:
            if(len(l)>35):
                return l[0:30]+'...'
            else:
                return l



    def clean():
        try:
            os.remove(picture_location+'temp.jpg')
            print('Clean success')
        except OSError as e:
            print('Already for download')

    def size_set(im):
        im=im.resize((480,300), Image.ANTIALIAS)
        return im


    def getTextInput():
        clean()
        input=textExample.get(1.0, END+"-1c")
        if('https://' in input or 'http://' in input):
            if(chVar_List.get()==1):
                playlist_search(input)
            else:
                html_search(input)
        else:
            key_search(input)

    def key_search(key):
        search = SearchVideos(key, offset = 1, mode = "json", max_results = 1)
        j=json.loads(search.result())
        for item in j["search_result"]:
                html_search(item["link"])

    def html_search(temp):
        global url
        url=temp
        yt=YouTube(temp)
        #指定圖片存放資料夾,抓取圖片網址,抓取圖片本身
        imageURL=yt.thumbnail_url
        img_data = requests.get(imageURL).content

        #創建目錄
        r=requests.get(imageURL)
        with open(picture_location+'temp.jpg','wb') as f:
        #將圖片下載下來
            f.write(r.content)
        
        #預覽圖片
        im=Image.open(picture_location+'temp.jpg')
        im=size_set(im)
        img=ImageTk.PhotoImage(im)
        imLabel.configure(image=img)
        imLabel.image=img
        title.config(text=long_set(yt.title))    


    def playlist_search(temp):
        global url
        url=temp
        t=1
        yt=YouTube(temp)
        imageURL=yt.thumbnail_url
        img_data = requests.get(imageURL).content

        #創建目錄
        r=requests.get(imageURL)
        with open(picture_location+'temp.jpg','wb') as f:
        #將圖片下載下來
            f.write(r.content)
        
        #預覽圖片
        im=Image.open(picture_location+'temp.jpg')
        im=size_set(im)
        img=ImageTk.PhotoImage(im)
        imLabel.configure(image=img)
        imLabel.image=img
        title.config(text=long_set(yt.title))    


        yt=Playlist(temp)

        li=Listbox(window,width=20,height=15,bg='black',fg='white',font=('Arial', 12))
        li.grid(row=3,column=2,rowspan=2,columnspan=2,pady=(20,0),sticky='N')
        for video in yt.videos:
            li.insert(END,str(t)+': '+video.title)
            li.insert(END,'')
            t=t+1
        window.update()



    def dl():
        global url
        global no_Image
        if(chVar_Image.get()==0):
            no_Image=False
        elif(chVar_Image.get()==1):
            no_Image=True


        if(chVar_List.get()==1):
            yt=Playlist(url)
            t=0
            for yt_video in yt.videos:
                title.config(text=long_set('Downloading--'+yt_video.title))
                window.update()
                stream=yt_video.streams.first()
                temp=stream.download(music_location)
                if(no_Image==False):
                    #將圖片下載下來
                    imageURL=yt_video.thumbnail_url
                    img_data = requests.get(imageURL).content
                    r=requests.get(imageURL)
                    with open(picture_location+'temp.jpg','wb') as f:
                        f.write(r.content)
                    os.chdir(picture_location)
                    #第一個split取得真正下載的檔案名稱,第二個split把.mp4換成.jpg
                    os.rename(picture_location+'temp.jpg',(temp.split(music_location)[1]).split('.mp4')[0]+'.jpg')
                os.chdir(road)
                video = VideoFileClip(temp)
                video.audio.write_audiofile(temp.split('.mp4')[0]+'.mp3')
                video.close()
                try:
                    os.remove(temp)
                except OSError as e:
                    l.config(text=e)
                t=t+1
            title.config(text='All Complete')
            window.update()

        else:
            yt=YouTube(url)
            title.config(text='Downloading--'+yt.title)
            stream=yt.streams.first()
            temp=stream.download(music_location)
            if(no_Image==False):
                os.chdir(picture_location)
                #第一個split取得真正下載的檔案名稱,第二個split把.mp4換成.jpg
                os.rename(picture_location+'temp.jpg',(temp.split(music_location)[1]).split('.mp4')[0]+'.jpg')
            os.chdir(road)
            video = VideoFileClip(temp)
            video.audio.write_audiofile(temp.split('.mp4')[0]+'.mp3')
            video.close()
            try:
                os.remove(temp)
            except OSError as e:
                l.config(text=e)
            else:
                textExample.delete('1.0',END)
                title.config(text='Complete')
    def Exit():
        window.destroy()
        home()
            


    btnRead=Button(window, height=1, width=10, text="Read", command=getTextInput)
    btnRead.grid(row=2,column=0,columnspan=2,pady=(5,0))

    final_check=Button(window, height=1, width=10, text="confirm", command=dl)
    final_check.grid(row=5,column=0,columnspan=2,pady=(5,0))

    #播放清單的確認
    PlayList_ch = Checkbutton(window, text='PlayList',var=chVar_List)
    PlayList_ch.grid(row=2,column=1,pady=(5,0))

    #不需要圖片的確認
    NoImage_ch = Checkbutton(window, text='No_Image',var=chVar_Image)
    NoImage_ch.grid(row=2,column=0,pady=(5,0))

    #主介面按鈕
    tem=Image.open(road+'/exit.png') 
    tem=tem.resize((75, 75), Image.ANTIALIAS)
    Exit_img=ImageTk.PhotoImage(tem)

    Exit_Button = tk.Button(window, width=75, height=75, command=Exit)
    Exit_Button.place(x=820,y=480)
    Exit_Button.configure(image=Exit_img)
    Exit_Button.image=Exit_img #keep a reference


    window.mainloop()
########################################################################################
def play_window():
    global musicList
    global running
    global road
    global i
    i=0
    running=True
    musicList = os.listdir(music_location)
    print(road)
    def divid(A):
        return A.split('.mp3')[0]



    def size_set(im):
        im=im.resize((480,300), Image.ANTIALIAS)
        return im

    #子標題的長度限制
    def long_set(l):        #所有的中文,日文,韓文
        jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3\u4e00-\u9fa5]')  # \uAC00-\uD7A3為匹配韩文的，其餘為日文
        if jap.search(l):
            if(len(l)>7):
                return l[0:5]+'...'
            else:
                return l
        else:
            if(len(l)>15):
                return l[0:12]+'...'
            else:
                return l

    #標題的長度限制
    def label_set(l):
        jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3\u4e00-\u9fa5]')  # \uAC00-\uD7A3為匹配韩文的，其餘為日文
        if jap.search(l):
            if(len(l)>20):
                return l[0:12]+'...'
            else:
                return l
        else:
            if(len(l)>35):
                return l[0:34]+'...'
            else:
                return l




    pygame.init()






    # 第1步，例項化object，建立視窗window
    window = tk.Tk()

    # 第2步，給視窗的視覺化起名字
    window.title('kiork\'s Window')

    # 第3步，設定視窗的大小(長 * 寬) *600x530
    window.geometry('1000x580')  # 這裡的乘是小x
    window.resizable(0,0)
    '''# 設定背景圖片
    temp=Image.open(road+'/'+'background3.jpg') 
    # temp=im=size_set(temp)
    temp=temp.resize((1000, 580), Image.ANTIALIAS)
    bg_image=ImageTk.PhotoImage(temp)

    background_label = tk.Label(window,image=bg_image)

    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #highlightthickness = 0
    '''


    class MyLabel(Label):
        def __init__(self, master, filename):
            im = Image.open(filename)
            seq =  []
            try:
                while 1:
                    seq.append(im.copy())
                    im.seek(len(seq)) # skip to next frame
            except EOFError:
                pass # we're done

            try:
                self.delay = im.info['duration']
            except KeyError:
                self.delay = 100

            first = seq[0].convert('RGBA')
            self.frames = [ImageTk.PhotoImage(first)]

            Label.__init__(self, master, image=self.frames[0])

            temp = seq[0]
            for image in seq[1:]:
                temp.paste(image)
                frame = temp.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))

            self.idx = 0

            self.cancel = self.after(self.delay, self.play)

        def play(self):
            self.config(image=self.frames[self.idx])
            self.idx += 1
            if self.idx == len(self.frames):
                self.idx = 0
            self.cancel = self.after(self.delay, self.play)        



    anim = MyLabel(window, music_bg)
    anim.place(x=0, y=0, relwidth=1, relheight=1)






    # 第4步，在圖形介面上設定標籤
    var = tk.StringVar()    # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
    l = tk.Label(window,textvariable=var, bg='black', fg='white', font=('Agency FB', 30), width=40, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    l.grid(row=0,column=0,columnspan=3,pady=10,padx=10)


    # 第4步，在圖形介面上設定標籤
    B_track = tk.Label(window,text='', bg='black', fg='white', font=('Agency FB', 20), width=20, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    B_track.grid(row=4,column=0,pady=5)

    # 第4步，在圖形介面上設定標籤

    N_track = tk.Label(window,text='', bg='black', fg='white', font=('Agency FB', 20), width=20, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    N_track.grid(row=4,column=2,pady=5)

    #播放條
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='black', background='DodgerBlue2')
    duration=ttk.Progressbar(window, style="red.Horizontal.TProgressbar",orient="horizontal",length=600,mode="determinate")
    duration.grid(row=2,column=0,columnspan=3,pady=10)
    duration['value']=0
    duration.start(interval=1000)



    #現在要放的歌(取NOW的值)
    pygame.mixer.music.load (music_location+musicList[i])

    #設定圖片
    Now= divid(musicList[i])
    try:
        im=Image.open(picture_location+Now+'.jpg')
    except:
        im=Image.open(road+'/background_jpg/no_image.jpg')
    im=size_set(im)
    img=ImageTk.PhotoImage(im)
    imLabel=tk.Label(window,image=img,highlightthickness=0)
    imLabel.configure(image=img)
    imLabel.image=img #keep a reference
    imLabel.grid(row=1,column=0,columnspan=3,pady=(0,20))
    #設定標籤
    var.set(label_set(Now))
    #設定第一首歌的播放條
    scale=int(AudioFileClip(music_location+musicList[i]).duration)
    duration['maximum']=scale
    
    t=1
    li=Listbox(window,width=35,height=9,bg='black',fg='white',font=('Arial', 12))
    li.grid(row=0,column=3,padx=(10,0),pady=(10,0),rowspan=2,sticky='N')
    for song in musicList:
        li.insert(END,str(t)+': '+divid(song))
        li.insert(END,'')
        t=t+1



    #上一首與下一首歌的標籤的準備
    def Hint():
        global loop
        global i
        if(loop==True):
            N_track.config(text='Loop')
        elif(i+1!=len(musicList)):
            N_track.config(text=long_set(divid(musicList[i+1])))
        else:
            N_track.config(text='No Track')

    
        if(loop==True):
            B_track.config(text='Loop')  
        elif(i-1!=-1):
            target=divid(musicList[i-1])
            B_track.config(text=long_set(divid(musicList[i-1])))
        else:
            B_track.config(text='No Track')


    #暫停&播放按鈕
    def pause_Play():
        global pause
        global stop_time
        if pause == False:
            pause = True
            stop_time=duration['value']
            pygame.mixer.music.pause()
            tem=Image.open(road+'/Play.png') 
            tem=tem.resize((50, 50), Image.ANTIALIAS)
            Play_img=ImageTk.PhotoImage(tem)
            pause_Button.configure(image=Play_img)
            pause_Button.image=Play_img #keep a reference
        else:
            pause = False
            pygame.mixer.music.unpause()
            tem=Image.open(road+'/pause.png') 
            tem=tem.resize((50, 50), Image.ANTIALIAS)
            pause_img=ImageTk.PhotoImage(tem)
            pause_Button.configure(image=pause_img)
            pause_Button.image=pause_img #keep a reference


    SONG_FINISHED = pygame.USEREVENT + 1
    # When a song is finished, pygame will add the
    # SONG_FINISHED event to the event queue.
    pygame.mixer.music.set_endevent(SONG_FINISHED)


    #播放條重設
    def Progress_reset():
        global i
        global p
        p=0
        scale=int(AudioFileClip(music_location+musicList[i]).duration)
        duration['value']=0
        duration['maximum']=scale
        window.update()

    #強制播放
    def pause_check():
        global pause
        global reset
        if(pause==True):
            pause=False
            reset=True
            tem=Image.open(road+'/pause.png') 
            tem=tem.resize((50, 50), Image.ANTIALIAS)
            pause_img=ImageTk.PhotoImage(tem)
            pause_Button.configure(image=pause_img)
            pause_Button.image=pause_img #keep a reference
            
    #音樂運行主體
    def music_main():
        global i
        global musicList
        #更新提示標籤
        Hint()
        #更新暫停鈕
        pause_check()
        #更新主圖片與主標籤
        Now=divid(musicList[i])
        var.set(label_set(Now)) 
        try:
            temp=Image.open(picture_location+Now+'.jpg')
        except:
            temp=Image.open(road+'/background_jpg/no_image.jpg')
        temp=im=size_set(temp)
        img=ImageTk.PhotoImage(temp)
        imLabel.configure(image=img)
        imLabel.image=img
        #更新播放條
        Progress_reset()
        #載入音樂
        pygame.mixer.music.load (music_location+musicList[i])
        pygame.mixer.music.play() #開始播放   

    def Next():
        global i
        global jumping
        global loop
        jumping=True
        if(loop==True):
            pygame.mixer.music.stop()
            music_main()   
        elif(i+1!=len(musicList)):
            pygame.mixer.music.stop()  
            i=i+1
            music_main()
        jumping=False

    def Back():
        global i
        global jumping
        global pause
        global loop
        jumping=True
        if(loop==True):
            pygame.mixer.music.stop()
            music_main()            
        elif(i-1!=-1):
            pygame.mixer.music.stop()
            i=i-1
            music_main()
        jumping=False

    def Auto():
        global i
        global jumping
        global loop
        global stop_time
        global reset
        while running:
            if(pause==True):
                duration['value']=stop_time
            elif(reset==True):
                Progress_reset()
                reset=False
            for event in pygame.event.get():
                if not jumping:
                    if event.type == SONG_FINISHED:# A track has ended
                        if(loop==True):
                            music_main()
                        elif(i+1!=len(musicList)):    
                            i=i+1
                            music_main()
                        else:
                            music_over()
                    

    def random_play():
        global jumping
        global i
        global pause
        i=0
        jumping=True #是否正在換歌
        random.shuffle(musicList)
        Hint()
        li.delete(0,END)
        t=1
        for song in musicList:
            li.insert(END,str(t)+': '+divid(song))
            li.insert(END,'')
            t=t+1
        music_main()
        jumping=False
        window.update()



    def loop():
        global loop
        if(loop==True):
            loop=False
            tem=Image.open(road+'/loop_off.png') 
            tem=tem.resize((40, 40), Image.ANTIALIAS)
            loop_img=ImageTk.PhotoImage(tem)
            loop_Button.configure(image=loop_img)
            loop_Button.image=loop_img #keep a reference
            Hint()
        else:
            loop=True
            tem=Image.open(road+'/loop_on.png') 
            tem=tem.resize((40, 40), Image.ANTIALIAS)
            loop_img=ImageTk.PhotoImage(tem)
            loop_Button.configure(image=loop_img)
            loop_Button.image=loop_img #keep a reference
            Hint()


    def select():
        global i
        global jumping
        jumping=True
        temp=li.curselection()[0]+1
        if(temp%2==1):
            temp=temp-(int(temp/2))-1
            i=temp
            music_main()
        jumping=False


    def Exit():
        global i
        i=-1
        pygame.mixer.music.stop()  
        window.destroy()
        home()


    def music_over():
        global i
        i=0
        Progress_reset()
        music_main()
        pause_Play()
        




    #上一首歌的按鈕
    tem=Image.open(road+'/Back.png') 
    tem=tem.resize((50, 50), Image.ANTIALIAS)
    Back_img=ImageTk.PhotoImage(tem)

    Back_Button = tk.Button(window, width=50, height=50, command=Back)
    Back_Button.grid(row=3,column=0)
    Back_Button.configure(image=Back_img)
    Back_Button.image=Back_img #keep a reference

    #暫停&播放的按鈕
    tem=Image.open(road+'/pause.png') 
    tem=tem.resize((50, 50), Image.ANTIALIAS)
    pause_img=ImageTk.PhotoImage(tem)

    pause_Button = tk.Button(window, width=50, height=50, command=pause_Play)
    pause_Button.grid(row=3,column=1)
    pause_Button.configure(image=pause_img)
    pause_Button.image=pause_img #keep a reference

    #下一首歌的按鈕
    tem=Image.open(road+'/Next.png') 
    tem=tem.resize((50, 50), Image.ANTIALIAS)
    Next_img=ImageTk.PhotoImage(tem)

    Next_Button = tk.Button(window, width=50, height=50, command=Next)
    Next_Button.grid(row=3,column=2)
    Next_Button.configure(image=Next_img)
    Next_Button.image=Next_img #keep a reference


    #主介面按鈕
    tem=Image.open(road+'/exit.png') 
    tem=tem.resize((75, 75), Image.ANTIALIAS)
    Exit_img=ImageTk.PhotoImage(tem)

    Exit_Button = tk.Button(window, width=75, height=75, command=Exit)
    Exit_Button.grid(row=3,column=3,rowspan=3,sticky='E')
    Exit_Button.configure(image=Exit_img)
    Exit_Button.image=Exit_img #keep a reference



    #隨機播放按鈕
    tem=Image.open(road+'/shuffle.png') 
    tem=tem.resize((40, 40), Image.ANTIALIAS)
    random_img=ImageTk.PhotoImage(tem)

    random_Button = tk.Button(window, width=40, height=40,command=random_play)
    random_Button.grid(row=1,column=2,pady=(0,20),sticky='SE')
    random_Button.configure(image=random_img)
    random_Button.image=random_img #keep a reference

    #循環播放按鈕
    tem=Image.open(road+'/loop_off.png') 
    tem=tem.resize((40, 40), Image.ANTIALIAS)
    loop_img=ImageTk.PhotoImage(tem)

    loop_Button = tk.Button(window, width=40, height=40,command=loop)
    loop_Button.grid(row=1,column=2,pady=(0,80),sticky='SE')
    loop_Button.configure(image=loop_img)
    loop_Button.image=loop_img #keep a reference

    #選歌播放按鈕
    select_Button=tk.Button(window, height=1, width=8, text="select",font=('Agency FB',18),command=select)
    select_Button.grid(row=0,column=3,pady=(200,0),rowspan=2,sticky='NE')


    t = threading.Thread(target = Auto,daemon=True)
    # 執行該子執行緒

    # 執行該子執行緒
    t.setDaemon(True)
    t.start()


    Hint()
    #####dura.config(text=(AudioFileClip(music+musicList[i]).duration))

    pygame.mixer.init() #對聲頻做初始化
    pygame.mixer.music.play() #開始播放
    Progress_reset()
    window.mainloop()


#######################################
def home():
    global i
    global pause
    global jumping
    global running
    global loop
    
    i=0
    pause=False
    jumping=False
    running=False
    loop=False
    def Download_open():
        window.destroy()
        download_window()


    def Play_open():
        window.destroy()
        play_window()

    window=Tk()
    window.geometry("1000x580")
    window.resizable(0,0)
    class MyLabel(Label):
        def __init__(self, master, filename):
            im = Image.open(filename)
            seq =  []
            try:
                while 1:
                    seq.append(im.copy())
                    im.seek(len(seq)) # skip to next frame
            except EOFError:
                    pass # we're done

            try:
                self.delay = im.info['duration']
            except KeyError:
                self.delay = 100

            first = seq[0].convert('RGBA')
            self.frames = [ImageTk.PhotoImage(first)]

            Label.__init__(self, master, image=self.frames[0])

            temp = seq[0]
            for image in seq[1:]:
                temp.paste(image)
                frame = temp.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))

            self.idx = 0

            self.cancel = self.after(self.delay, self.play)

        def play(self):
            self.config(image=self.frames[self.idx])
            self.idx += 1
            if self.idx == len(self.frames):
                self.idx = 0
            self.cancel = self.after(self.delay, self.play)        



    anim = MyLabel(window, main_bg)
    anim.place(x=0, y=0, relwidth=1, relheight=1)


    #主介面標題
    l = tk.Label(window,text='kiork\'s music cafe', bg='black', fg='white', font=('Agency FB', 35), width=30, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    l.grid(row=0,column=0,pady=30,sticky='W')

    #按鈕的標籤提示
    l = tk.Label(window,text='Music', bg='black', fg='white', font=('Agency FB', 17), width=20, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    l.grid(row=2,column=0,padx=(450,0),pady=(5,0),sticky='S')
    #按鈕的標籤提示
    l = tk.Label(window,text='Download', bg='black', fg='white', font=('Agency FB', 17), width=20, height=1)
    # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
    l.grid(row=2,column=1,padx=(105,0),pady=(5,0),sticky='S')

    #介面切換按鈕
    tem=Image.open(road+'/music.png') 
    tem=tem.resize((75, 75), Image.ANTIALIAS)
    Play_img=ImageTk.PhotoImage(tem)

    Play_Button = tk.Button(window, width=85, height=85, command=Play_open)
    Play_Button.grid(row=1,column=0,padx=(450,0),pady=(300,0))
    Play_Button.configure(image=Play_img)
    Play_Button.image=Play_img #keep a reference

    tem=Image.open(road+'/download.png') 
    tem=tem.resize((75, 75), Image.ANTIALIAS)
    dl_img=ImageTk.PhotoImage(tem)

    dl_Button = tk.Button(window, width=85, height=85, command=Download_open)
    dl_Button.grid(row=1,column=1,padx=(105,0),pady=(300,0))
    dl_Button.configure(image=dl_img)
    dl_Button.image=dl_img #keep a reference




    # 第6步，主視窗迴圈顯示
    window.mainloop()





if __name__ == "__main__":
    home()
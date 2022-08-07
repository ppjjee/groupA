import streamlit as st
from st_clickable_images import clickable_images
import os, glob, pathlib, random, pickle, time, requests, json, commons
import io
from io import StringIO, BytesIO
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
import uuid
from itertools import chain
from sftp import SFTP
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
</style>
"""

st.set_page_config(initial_sidebar_state="collapsed")

# set session_state for change pages
st.session_state.update(st.session_state)
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    

# callback functions for change page
def CB_Home():
    st.session_state.active_page = 'Page_1'

def CB_Page1():
    st.session_state.active_page = 'Page_2'

def CB_Page2():
    st.session_state.active_page = 'Page_3'

def CB_Page3():
    st.session_state.active_page = 'Page_4'

def CB_Page4():
    st.session_state.active_page = 'Page_5'

def CB_Page5():
    st.session_state.active_page = 'Page_6'

def CB_Page6():
    st.session_state.active_page = 'Page_7'

def CB_Page7():
    st.session_state.active_page = 'Page_8'

def CB_Page8():
    st.session_state.active_page = 'Page_9'

def CB_Page9():
    st.session_state.active_page = 'Page_10'


sftp = SFTP(st.secrets["HOSTNAME"], st.secrets["USERNAME"], st.secrets["PASSWORD"])

def home():
    result_file_name = str(uuid.uuid4()) + ".json"
    save_path = get_result_dir() + "/" + result_file_name
    
    header = st.container()
    with header:
        title = st.title('We recommend music that matches the image.')
        st.markdown(hide_menu, unsafe_allow_html = True)

        sh1 = st.container()
        with sh1:
            subheader1 = st.subheader('Informed Consent 📝')
            st.text("This is an Yonsei University research project.")
            st.text("All data for research is collected anonymously for research purposes.")
            st.text("For questions, please contact park.je@yonsei.ac.kr.")
            st.text("If you are under 18 years old, you need consent from your parents to participate.")
            st.text("Those who participate in the experiment are deemed to have consented to proceed with the experiment.")
            st.write('-----')

        sh2 = st.container()
        with sh2:
            subheader2 = st.subheader('What you are going to do 🧪')
            st.text("In this experiment, we recommend musics that matches an image.") 
            st.text("We give you several kinds of image choices.")
            st.text("Select an image you like the most, then keywords will show up that match the selected image (up to 3).")
            st.text("If you are not satisfied with the keywords, you can change them from the selection.")
            st.text("When keyword selection is complete, we will automatically recommend musics that match the image.")
            st.write('-----')


        sh3 = st.container()
        with sh3:
            subheader3 = st.subheader('Warning 👀👂')
            st.text("If you SKIP A STEP, NO COMPENSATION will be provided.")
            st.text("If you DO NOT FOLLOW THE PROCESS, YOU MAY SEE AN ERROR MESSAGE AND YOUR PARTICIPATION IN THE EXPERIMENT MAY NOT BE COMPLETED.")
            st.write('-----')

        st.experimental_set_query_params(path=save_path)
        st.button('Agree, Start', on_click=CB_Home)
 
 ## ------------------ for Mood Image Retrieval ------------------------ 
def get_result_dir():
    path = os.getcwd() + "/results"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    print("created result dir: " + path)
    return path

mood_imgs = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/calm.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/dark.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fast.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun_funny_party.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/melodic.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/relaxing.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/romantic_holiday_travel.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sad.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sad_emotional.jpg?raw=true'              
            ]
mood_imgs2 = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/dark_calm_nature.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/funny.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/groovy_happy.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/love_retro_melodic.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/nature_dramatic_dark.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/retro_love_melodic.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sad_calm.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sexy.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/slow.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/soft.jpg?raw=true'
            ]           
theme_imgs = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/adventure_action.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/christmas.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/corporate_children.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/holiday_summer_travel.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/movie.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/nature.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/party.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/sport.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer_party.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/trailer_film_background.jpg?raw=true'
            ]
theme_imgs2 = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/children.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/film.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/game.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/love.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/movie_background_film.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/nature_dark.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/space.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/sport_action_adventure.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer_holiday_travel.jpg?raw=true',
            ]

def image_page(imgs, cb):
    # show frontend title 
    st.title('Image to Music Retrieval')
    st.text("✔️ Please select an image! We recommend music that matches the selected image.")
    st.text("✔️ After selecting an image, please wait for a while until the next process.")
    st.markdown(hide_menu, unsafe_allow_html = True)  

    save_path = st.experimental_get_query_params()['path'][0]
    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 Loooooooooooooooooooaaaaaaaaaaaaaaaaaaaading... 👀')
        try:
            all_tags = []
            tag_list = []
            for i in imgs:
                a= i.split('/')[-1]
                b = a.split('?')[0]
                c = b.split('.')[0]
                tag_list.append(c)

            for j in tag_list:
                a = j.split('_')
                all_tags.append(a)
        

            # display images that can be clicked on using 'clickable_images' func
            clicked = clickable_images(paths=imgs, 
                                        titles=[f"Image {str(i)}" for i in range(1, len(imgs)+1)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px"})  
            

            model_load_state.success("Please click an image you like. We'll recommend music that matches the image.")
            selected_tags = all_tags[clicked]

            final_tag = []
            for tag in selected_tags:
                tup = (tag, 0)
                final_tag.append(tup)
            
                
            # if some image is clicked,
            if clicked >= 0:
                model_load_state.info(f"**Keywords of Image {str(int(clicked)+1)} Are Below.**")
                # show final tags of selected image
                show_tags = st.container()
                print(show_tags)
                with show_tags:
                    if len(final_tag) == 3:
                        st.write('-----')
                        model_load_state.info("**Scroll Down and Press the Button**")                  
                        # save results
                        if st.checkbox("Do you want to move to the next page?", key='check1'):
                            results_A = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': final_tag[1][0], 'Tag3': final_tag[2][0]}
                            if not os.path.exists(save_path):
                                data = {}
                                data['submits'] = []
                                data['submits'].append(results_A)
                                print("no exists", data)
                                with open(save_path, 'w') as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)

                            else:
                                data = {}
                                with open(save_path, "r") as json_file:
                                    data = json.load(json_file)
                                data['submits'].append(results_A)
                                print("exists, before", data)

                                with open(save_path, "w") as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)
                                    print("exists, after", data)
                    
                    elif len(final_tag) == 2:
                        st.write('-----')
                        model_load_state.info("**Scroll Down and Press the Button**")                  
                        # save results
                        if st.checkbox("Do you want to move to the next page?", key='check2'):
                            if not os.path.exists(save_path):
                                results_A = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': final_tag[1][0], 'Tag3': '-'}
                                data = {}
                                data['submits'] = []
                                data['submits'].append(results_A)
                                print("no exists", data)
                                with open(save_path, 'w') as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)

                            else:
                                data = {}
                                with open(save_path, "r") as json_file:
                                    data = json.load(json_file)
                                data['submits'].append(results_A)
                                print("exists, before", data)

                                with open(save_path, "w") as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)
                                    print("exists, after", data)
                            
                            
                    else:
                        st.write('-----')                
                        model_load_state.info("**Scroll Down and Press the Button**")                  
                        # save results
                        if st.checkbox("Do you want to move to the next page?", key='check3'):
                            results_A = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': '-', 'Tag3': '-'}
                            if not os.path.exists(save_path):
                                data = {}
                                data['submits'] = []
                                data['submits'].append(results_A)
                                print("no exists", data)
                                with open(save_path, 'w') as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)

                            else:
                                data = {}
                                with open(save_path, "r") as json_file:
                                    data = json.load(json_file)
                                data['submits'].append(results_A)
                                print("exists, before", data)

                                with open(save_path, "w") as save_f:
                                    json.dump(data, save_f, ensure_ascii=False, indent=4)
                                    print("exists, after", data)
                            
                    st.experimental_set_query_params(path=save_path)                               
                    st.button('NEXT', on_click=cb)

            else:
                model_load_state.info(f"**There is no image selected. Please select one image.**")
                
                
                
            

        except:
            message_container = st.empty() 
            message = message_container.write('👉 Please, wait. Loading... 👀')
            if message != '':
                time.sleep(23)
                message_container.empty()





## ------------------ for Mood Music Retrieval ------------------------    
def TagLoad(path):
    f = open(path)
    data = json.load(f)
    a = data['submits'][-1]['Tag1'] 
    tag1 = list(a.split(" "))
    b = data['submits'][-1]['Tag2']
    tag2 = list(b.split(" "))
    c = data['submits'][-1]['Tag3']
    tag3 = list(c.split(" "))
    tags = []
    tags.append(tag1)
    tags.append(tag2)
    tags.append(tag3) # c_tags = [['calm'], ['advertising']]

    def flatten_list(_2d_list):
        flat_list = []
        # Iterate through the outer list
        for element in _2d_list:
            if type(element) is list:
                # If the element is of type list, iterate through the sublist
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return flat_list

    f_tags = flatten_list(tags)     #f_tags = ['calm', 'advertising']
    print('f_tags is', f_tags)
    list_set = set(f_tags) # ['calm', 'advertising', 'calm] 일 경우, ['calm', 'advertising']
    music_tag = list(list_set)
    music_tag[:] = (value for value in music_tag if value != "-") # ['-']는 제외함
    return music_tag



# def music_retrieval():
#     remoteFilePath = '/nas2/epark/mtg-jamendo-dataset/data/autotagging_moodtheme.tsv'
#     localFilePath = 'autotagging_moodtheme.tsv'
#     sftp.download(remoteFilePath, localFilePath)
#     tracks, tags, extra = commons.read_file(localFilePath)

#     find_tag_list = []
#     save_path = st.experimental_get_query_params()['path'][0]
#     print("save path: " + save_path)
#     music_tag = TagLoad(save_path)
#     for i in music_tag:
#         p = tags['mood/theme'][i]
#         q = list(p)
#         find_tag_list.extend(q)
#         print('find_tag_list', find_tag_list)
        
#     if len(find_tag_list) == 3:
#         a, b, c = find_tag_list
#         elements_in_all = list(set.intersection(*map(set, [a, b, c])))
#         elements_in_two = list(set.intersection(*map(set, [a, b])))
#         elements_in_two_2nd = list(set.intersection(*map(set, [b, c])))
#         elements_in_two_3rd = list(set.intersection(*map(set, [a, b])))
#         elements_in_one = a
        
#         if len(elements_in_all) !=0 and len(elements_in_all) >= 5:
#             random_all = random.choices(elements_in_all, k=5)
#         elif len(elements_in_all) == 0 and len(elements_in_two) != 0  and len(elements_in_two) >= 5:
#             random_all = random.choices(elements_in_two, k=5)
#         elif len(elements_in_all) ==0 and len(elements_in_two) ==0 and len(elements_in_two_2nd) >= 5:
#             random_all = random.choices(elements_in_two_2nd, k=5)
#         elif len(elements_in_all) ==0 and len(elements_in_two) ==0 and len(elements_in_two_2nd) ==0 and len(elements_in_two_3rd) >=5:
#             random_all = random.choices(elements_in_two_3rd, k=5)
#         else:
#             random_all = random.choices(elements_in_one, k=5)

        
#     elif len(find_tag_list) == 2:
#         a, b = find_tag_list
#         elements_in_all = list(set.intersection(*map(set, [a, b])))
#         elements_in_one = a
#         elements_in_one_2nd = b
        
#         if len(elements_in_all) !=0 and len(elements_in_all) >= 5:
#             random_all = random.choices(elements_in_all, k=5)
#         elif len(elements_in_all) == 0 and len(elements_in_one) >= 5:
#             random_all = random.choices(elements_in_one_2nd, k=5)
#         else: 
#             random_all = random.choices(elements_in_one, k=5)

        
#     else:
#         a = find_tag_list
#         elements_in_all = a
#         random_all = random.choices(elements_in_all, k=5)
#         music_tags = st.container()

#     return random_all, save_path
    
# def createAudio(filename):
#     remoteFilePath = sftp.dirRemoteMusicData + '/' + filename
#     localFilePath = sftp.dirMusic + '/' + filename
#     sftp.download(remoteFilePath, localFilePath)
#     audio_file = open(localFilePath, 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/ogg', start_time=0)

# ## streamlit display codes
# def music_page(cb):
#     random_all, save_path = music_retrieval()
#     st.title('Image to Music Retrieval')
#     st.subheader("Now, we recommend a music list that matches the image!")
#     st.write('-----')
#     st.text("🎧 Please enjoy the music and answer the questions below. 🎧")
#     st.markdown(hide_menu, unsafe_allow_html = True)  

#     for i in range(5):
#         createAudio(str(random_all[i]) + '.mp3')

#     st.write('-----')

#     ## save results
#     with st.container():
#         satis_result = st.slider('Do you satisfy with the recommended music?', min_value=0, max_value=100, value=50, step=1)
#         st.write('-----')
#         if st.checkbox("Do you want to move to the next page?", key='check4'):
#             with open(save_path, "r") as json_file:
#                 results_B = {'Music Satisfaction': satis_result}
#                 data = json.load(json_file)
#                 data['submits'][-1].update(results_B)

#             with open(save_path, "w") as save_f:
#                 json.dump(data, save_f, ensure_ascii=False, indent=4)    
#                 print("exists, after", data)
            
#             st.experimental_set_query_params(path=save_path)
#             st.button('NEXT', on_click=cb)
def music_retrieval():
    save_path = st.experimental_get_query_params()['path'][0]
    music_tag = TagLoad(save_path) # 수정한 image tag list를 music_tag로 활용함
    
    music_list = glob.glob("/nas3/epark/workspace/retreival/music_test/*")
    music_tag_list = []
    for i in music_list:
        a = i.split('/')[-1].split('-')[0]
        music_tag_list.append(a) # music_tag_list = ['balad_sad', 'ballad_sad_uplifting'...]
         
    music_final_tag_list = []
    for i in music_tag_list:
        a = i.split('_')
        music_final_tag_list.append(a) # music_final_tag_list = [['ballad', 'sad'], ['ballad', 'sad', 'uplifting'], ...]
    
    
    all_tags = 0
    all_tags_list = []
    two_tags = 0
    two_tags_list = []
    one_tags = 0
    one_tags_list = []
    for i in music_final_tag_list:
        set_1 = set(i)
        set_2 = set(music_tag)
        if (set_1 & set_2):
            if len(set_1 & set_2) == 3:
                print(set_1 & set_2)
                print('all_tags: ' + str(all_tags))
                all_tags_list.append(all_tags) # all_tag_list = [0, 1, 3, 4, 6, ...]
            elif len(set_1 & set_2) == 2:
                print(set_1 & set_2)
                print('two_tags: ' + str(two_tags))
                two_tags_list.append(two_tags) # two_tags_list = [2, 5, 9 ,...]
            else:
                print(set_1 & set_2)
                print('one_tags: ' + str(one_tags))
                one_tags_list.append(one_tags) # one_tags_list = [7, 8, 10, ...]
            all_tags = all_tags+1
            two_tags = two_tags+1
            one_tags = one_tags+1
        else:
            all_tags = all_tags+1
            two_tags = two_tags+1
            one_tags = one_tags+1

    if len(all_tags_list) !=0 and len(all_tags_list) >= 3: 
        random_all = random.choices(all_tags_list, k=3)
    elif len(all_tags_list) < 3 and len(two_tags_list) >= 3:
        random_all = random.choices(two_tags_list, k=3)
    elif len(all_tags_list) < 3 and len(two_tags_list) < 3 and len(one_tags_list) >=3 :
        random_all = random.choices(one_tags_list, k=3)
    # else:
    #     random_all = random.choices(one_tags_list, k=3)
    
    filename = []
    for i in random_all:
        a = music_list[i].split('/')[-1]
        filename.append(a)
        
    return filename, save_path # retun 5 selected music names 

def createAudio(filename):
    remoteFilePath = sftp.dirRemoteMusicData + '/' + filename
    localFilePath = sftp.dirMusic + '/' + filename
    sftp.download(remoteFilePath, localFilePath)
    print(remoteFilePath)
    audio_file = open(localFilePath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg', start_time=0)

def music_page(cb):
    filename, save_path = music_retrieval()
    st.title('Image to Music Retrieval')
    st.subheader("Now, we recommend a music list that matches the image!")
    st.write('-----')
    st.text("🎧 Please enjoy the music and answer the questions below. 🎧")
    st.markdown(hide_menu, unsafe_allow_html = True)

    for i in range(3):
        createAudio(filename[i])

    st.write('-----')

    ## save results
    with st.container():
        satis_result = st.slider('Do you think the retrieved music represents the selected image well?', min_value=0, max_value=100, value=50, step=1)
        st.write('-----')
        if st.checkbox("Do you want to move to the next page?", key='check4'):
            with open(save_path, "r") as json_file:
                results_B = {'Music Satisfaction': satis_result}
                data = json.load(json_file)
                data['submits'][-1].update(results_B)

            with open(save_path, "w") as save_f:
                json.dump(data, save_f, ensure_ascii=False, indent=4)    
                print("exists, after", data)
            
            st.experimental_set_query_params(path=save_path)
            st.button('NEXT', on_click=cb)


## ------------------ for Survey ------------------------ 
def survey_page():
    save_path = st.experimental_get_query_params()['path'][0]
    print("path 5: " + save_path)
    st.title('Image to Music Retrieval')
    st.subheader("please respond to the questionnaire consisting of 4 sections.")
    st.subheader("💪 You are almost there! 💪")
    st.markdown(hide_menu, unsafe_allow_html = True)  

    survey = st.container()
    with survey:
        st.write('-----')
        
        gender = st.radio(
            "What's your gender?",
            ('Male', 'Female', 'Non-binary/Third gender'))

        age = st.radio(
            "What's your age group?",
            ('10s', '20s', '30s', '40s', '50s', '60s', 'Above 60s'))

        education = st.radio(
            "What's the highest level of education that you have completed?",
            ('Less than high school', 'High school graduate', 'Some college', '2 year degree', '4 year degree', 'Professional degree', 'Doctorate'))
            # ('Primary/Elementary education not completed', 'Primary/Elementary education', 'Secondary education','Further education (Bachelor degree, diploma', 'Higher education (Masters, Doctorate)'))

        ethnicity = st.radio(
            "What's your Ethnicity (or Race)?",
            ('Prefer not to disclose', 'American Indigenous (Alaskan Native / Native American)', 'Asian', 'Black', 'Latinx / Hispanic', 'Middle Eastern / North African', 'Pacific Islander', 'White / Caucasian', 'Multi Race / Ethnicity'))
        st.write('-----')

        
        satisfaction1 = st.radio(
            "I'm very satisfied with this image-music retrievel system.",
            ('Very satisfied', 'Satisfied', 'Neutral', 'Unsatisfied', 'Very unsatisfied'))

        satisfaction2 = st.radio(
            "This image-music retrieval system meet my expectation.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction3 = st.radio(
            "This image-music retrieval system work the way I want it to work.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction4 = st.radio(
            "My experience with this image music retrieval system is very pleasing.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction5 = st.radio(
            "This image music retrieval system does a satisfactory job of fulfilling my needs.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')
        
        
        ItU1 = st.radio(
            "I intend to use this image-music retrieval system in the future.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU2 = st.radio(
            "I plan to use this image-music retrieval system when it starts to service.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU3 = st.radio(
            "I would recommend this image-music retrieval system to others.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU4 = st.radio(
            "I intend to continue using this image music retrieval system rather than discontinue its use.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')
        
        
        valence1 = st.radio(
            "After using this image music retrieval system, I feel that I have had a good experience.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        valence2 = st.radio(
            "I believe that this image music retrieval system provider tries to give me a good experience.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        valence3 = st.radio(
            "I believe that this image music retrieval system provider knows the type of experience its users want.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')


        ## save results
        if st.checkbox("Do you want to move to the next page?", key='fin'):
            results_B = {'gender': gender, 'age': age, 'education': education, 'ethnicity': ethnicity,
             'satisfaction1': satisfaction1, 
             'satisfaction2': satisfaction2, 
             'satisfaction3': satisfaction3, 
             'satisfaction4': satisfaction4, 
             'satisfaction5': satisfaction5, 
             'ItU1': ItU1, 
             'ItU2': ItU2, 
             'ItU3': ItU3,
             'ItU4': ItU4,
             'valence1': valence1,
             'valence2': valence2,
             'valence3': valence3,
             }
            with open(save_path, "r") as json_file:
                data = {}
                data = json.load(json_file)
            data['submits'].append(results_B)

            with open(save_path, "w") as save_f:
                json.dump(data, save_f, ensure_ascii=False, indent=4)
                print("exists, after", data)
            
            sftp.upload(save_path, sftp.dirRemoteSurveyResult + '/' + str(uuid.uuid4()) + ".json")
            st.button('END', on_click=CB_Page9)  
                                                



## ------------------ for Final ------------------------ 
def final_page():
    st.balloons()
    st.title("Thank you for your participation!")
    st.markdown(hide_menu, unsafe_allow_html = True)         

                                                
# run the active page
if st.session_state.active_page == 'Home':
    home()
elif st.session_state.active_page == 'Page_1':
    image_page(mood_imgs, CB_Page1)
elif st.session_state.active_page == 'Page_2':
    music_page(CB_Page2)
elif st.session_state.active_page == 'Page_3':
    image_page(mood_imgs2, CB_Page3)
elif st.session_state.active_page == 'Page_4':
    music_page(CB_Page4)
elif st.session_state.active_page == 'Page_5':
    image_page(theme_imgs, CB_Page5)
elif st.session_state.active_page == 'Page_6':
    music_page(CB_Page6)
elif st.session_state.active_page == 'Page_7':
    image_page(theme_imgs2, CB_Page7)
elif st.session_state.active_page == 'Page_8':
    music_page(CB_Page8)
elif st.session_state.active_page == 'Page_9':
    survey_page()
elif st.session_state.active_page == 'Page_10':
    final_page()
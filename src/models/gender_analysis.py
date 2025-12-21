import re
from typing import List, Set, Dict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import mannwhitneyu
import os
import sys
sys.path.append(os.path.abspath(".."))
from src.utils.general_utils import *


class GenderAnalysis:
    """
    A class grouping utility functions for detecting and analyzing gendered language in text.
    """

    def __init__(self):
        # Word lists from Danielle Sucher's "Jailbreak the Patriarchy" augmented
        self.male_terms = [
            'guy', 'spokesman', 'chairman', "men's", 'men', 'him', "he's", 'his', 'boy',
            'boyfriend', 'boyfriends', 'boys', 'brother', 'brothers', 'dad', 'dads',
            'dude', 'father', 'fathers', 'fiance', 'gentleman', 'gentlemen', 'god',
            'grandfather', 'grandpa', 'grandson', 'groom', 'he', 'himself', 'husband',
            'husbands', 'king', 'male', 'man', 'mr', 'nephew', 'nephews', 'priest',
            'prince', 'son', 'sons', 'uncle', 'uncles', 'waiter', 'widower', 'widowers',
            'congressman',

            # --- Added universal & contextual male terms ---
            'bloke', 'chap', 'fella', 'gent', 'sir', 'lad', 'lads',
            'manliness', 'masculine', 'boyhood',
            'father-in-law', 'stepfather', 'stepson',
            'godfather', 'old man',
            'bachelor', 'groomsman',
            'kings',
            'monk', 'wizard',
            'policeman', 'fireman', 'salesman', 'businessman', 'workman',

            # --- Public figures ---
            "bush", "sanders",
            "einstein", "hitchcock", "bansky", "kanye", "obama","biden","trump","putin","zelenskyy",
            "macron","schwarzenegger","clooney","hanks","dicaprio",
            "pitt","depp","cruise","stallone","eastwood","gosling","carey","seinfeld","rock","chappelle",
            "sandler","springsteen","dylan","cobain","mars","drake","sheeran","mccartney","lennon",
            "jagger","bale","damon","affleck","reynolds","washington","freeman","jackson","smith","murphy",
            "reeves","keaton","downey","ruffalo","leno","colbert","stewart","oppenheimer","gates","musk"


            # --- 200 Most Popular American male names ---
            "james","robert","john","michael","david","william","richard","joseph","thomas","charles",
            "christopher","daniel","matthew","anthony","mark","donald","steven","paul","andrew","joshua",
            "kenneth","kevin","brian","george","edward","ronald","timothy","jason","jeffrey","ryan",
            "jacob","gary","nicholas","eric","jonathan","stephen","larry","justin","scott","brandon",
            "benjamin","samuel","gregory","alexander","frank","patrick","raymond","jack","dennis","jerry",
            "tyler","aaron","jose","adam","nathan","henry","douglas","zachary","peter","kyle",
            "walter","ethan","jeremy","harold","keith","christian","roger","noah","gerald","carl",
            "terry","sean","austin","arthur","lawrence","jesse","dylan","bryan","joe","jordan",
            "billy","bruce","albert","willie","gabriel","logan","alan","juan","wayne","roy",
            "ralph","randy","eugene","vincent","bobby","russell","louis","philip","johnny","riley",
            "victor","mason","dale","brett","caleb","curtis","phillip","nathaniel","rodney","cody",
            "joel","craig","tony","evan","shawn","wesley","alex","travis","chad","derrick",
            "stanley","leonard","connor","oscar","xavier","miguel","edwin","martin","emmanuel","jay",
            "clifford","herman","seth","edgar","mario","frederick","allen","tyrone","max","aiden",
            "colton","hector","jon","spencer","rick","clarence","malik","leo","dustin","maurice",
            "dominic","hayden","troy","gordon","marshall","abel","andre","lawson","reed","ramon",
            "lance","casey","terrence","francis","trevor","jared","marco","darren","eli","ben",
            "rafael","don","diego","romeo","ruben","clayton","carlos","kirk","brayden","ronnie",
            "felix","jimmy","asher","camden","harvey","brendan","tristan","dean","parker","francisco",
            "ivan","milo","ted"
        ]

        self.female_terms = [
            'heroine', 'spokeswoman', 'chairwoman', "women's", 'actress', 'women',
            "she's", 'her', 'aunt', 'aunts', 'bride', 'daughter', 'daughters', 'female',
            'fiancee', 'girl', 'girlfriend', 'girlfriends', 'girls', 'goddess',
            'granddaughter', 'grandma', 'grandmother', 'herself', 'ladies', 'lady',
            'mom', 'moms', 'mother', 'mothers', 'mrs', 'ms', 'niece', 'nieces',
            'priestess', 'princess', 'queens', 'she', 'sister', 'sisters', 'waitress',
            'widow', 'widows', 'wife', 'wives', 'woman',

            # --- Added universal & contextual female terms ---
            'gal', 'lass', 'lassie',
            'ma’am', 'madam', 'mademoiselle', 'madame',
            'femininity', 'feminine', 'girlish', 'womanhood',
            'matriarch', 'stepmother', 'mother-in-law', 'stepdaughter',
            'goddaughter',
            'bachelorette', 'bridesmaid',
            'queen',  # singular queen missing
            'nun', 'witch',
            'policewoman', 'firewoman', 'saleswoman', 'businesswoman', 'workwoman',
            'hen'  # slang, sometimes used in cartoons for women
        
            # --- Public figures ---
            "clinton","pelosi","warren","merkel","ardern","whitman","winfrey","streep","roberts","kidman",
            "bullock","blunt","portman","johansson","lawrence","stone","barrymore","aniston","kardashian","beyoncé",
            "adele","rihanna","swift","gaga","madonna","perry","grande","minaj","dion","carey",
            "kaling","fey","poehler","degeneres","booker","rowling","atwood","angelou","steinem","torres",
            "lopez","hudson","zeta-jones","theron","cuoco","watson","winslet","deschanel","witherspoon","mcadams"

            # --- 200 Most Popular American female names ---
            "mary","patricia","jennifer","linda","elizabeth","barbara","susan","jessica","sarah","karen",
            "nancy","margaret","lisa","betty","dorothy","sandra","ashley","kimberly","donna","emily",
            "michelle","carol","amanda","melissa","deborah","stephanie","rebecca","laura","helen","sharon",
            "cynthia","kathleen","amy","shirley","angela","anna","brenda","pamela","nicole","emma",
            "samantha","katherine","christine","debra","rachel","catherine","carolyn","janet","ruth","maria",
            "heather","diane","virginia","julie","joyce","victoria","kelly","christina","lauren","joan",
            "evelyn","olivia","judith","megan","cheryl","martha","andrea","frances","hannah","jacqueline",
            "ann","jean","alice","kathryn","gloria","teresa","sara","janice","doris","julia",
            "madison","grace","amber","tiffany","beverly","denise","marilyn","danielle","charlotte","caroline",
            "lori","kayla","alexis","sophia","kim","rose","hailey","brianna","cindy","kara",
            "erin","leslie","katie","lillian","sydney","morgan","judy","casey","natalie","brittany",
            "jordan","isabella","dana","veronica","lydia","valerie","brooke","autumn","irene","kristen",
            "kendra","kylie","paige","mia","sabrina","holly","faith","naomi","riley","makayla",
            "jasmine","molly","isabelle","aubrey","harper","addison","peyton","avery","keira","skylar",
            "bailey","eliza","clara","hadley","nina","willow","sadie","delilah","arianna","stella",
            "vivian","eleanor","lucy","adeline","elena","violet","zoey","madeline","cora","maryann",
            "lucia","summer","genevieve","annabelle","mariah","hazel","luna","mackenzie","allison","isla",
            "rebecca","leah","sophie","eva","ruby","aria","caroline","ruth","daisy","ivy",
            "margot","norah","june","everly", "hillary"
        ]
        
            # Precompile regex patterns
        
        male_pattern = r"\b(?:{})\b".format("|".join(map(re.escape, self.male_terms)))
        female_pattern = r"\b(?:{})\b".format("|".join(map(re.escape, self.female_terms)))

        self.male_regex = re.compile(male_pattern, flags=re.IGNORECASE)
        self.female_regex = re.compile(female_pattern, flags=re.IGNORECASE)
        
        # Basic list of common English stopwords
        self.STOPWORDS = {
        # --- pronouns and determiners ---
        "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
        "yourself","yourselves","he","him","his","himself","she","her","hers","herself",
        "it","its","itself","they","them","their","theirs","themselves","us",
        "what","which","who","whom","this","that","these","those",
        
        # --- auxiliary verbs & modals ---
        "am","is","are","was","were","be","been","being","have","has","had","having",
        "do","does","did","doing","can","could","will","would","shall","should","may",
        "might","must","ought",
        
        # --- articles, prepositions, conjunctions ---
        "a","an","the","and","but","if","or","because","as","until","while","of","at",
        "by","for","with","about","against","between","into","through","during","before",
        "after","above","below","to","from","up","down","in","out","on","off","over",
        "under","again","further","then","once","here","there","when","where","why",
        "how","all","any","both","each","few","more","most","other","some","such","no",
        "nor","not","only","own","same","so","than","too","very","s","t","now","just",
        
        # --- contractions & spoken forms ---
        "im","ive","id","youre","youve","youd","hes","shes","theyre","theyve","weve",
        "wed","dont","doesnt","didnt","cant","couldnt","wont","wouldnt","shouldnt",
        "isnt","arent","wasnt","werent","thats","theres","whats","whos","hows","lets",
        "re","don","ill","ll","d","ve","y","ma",
        
        # --- generic filler verbs & expressions ---
        "get","got","getting","go","goes","going","gone","see","saw","seen","say",
        "says","said","make","makes","made","know","knows","knew","think","thinks",
        "thought","need","needs","needed","want","wants","wanted","like","likes",
        "liked","use","used","using","try","trying","tried","work","works","worked",
        "take","takes","took","put","puts","doing","done","give","gives","gave",
        
        # --- discourse fillers ---
        "well","really","one","even","still","lot","thats","thing","things","way",
        "something","anything","everything","nothing","time","back","new","also",
        "ever","always","maybe"
        }

        # aggregated topics for man an woman
        self.agg_topic_female = {
            # 1. Female archetypes
            # "47_bee_queen bee_queen_bees": "Female archetypes",
            # "88_of herself_herself_her everywhere_herself she": "Female archetypes",
            # "40_then she_then_and then_told her": "Female archetypes",
            # "52_hey lady_cake_hey_lady": "Female archetypes",
            # "60_ma am_ma_am_buy it": "Female archetypes",
            "3_women_woman_female_girls": "Women archetypes",

            # Politic
            "5_hillary_for hillary_voted_voted for": "Politics",

            # Public Figures
            # "83_kardashian_kim_the kardashian_kim kardashian": "Public Figures",

            # Royalty
            "1_queen_the queen_my queen_majesty": "Royalty",

            # 2. Family roles
            "-1_she_her_mother_mom": "Family roles",
            "11_sister_your sister_sisters_my sister": "Family roles",
            "14_grandma_grandmother_great great_great": "Family roles",
            "16_about your_your mother_about_tell me": "Family roles",
            # "87_granddaughter_my granddaughter_my daughter_daughter": "Family roles",
            # "70_aunt_jemima_aunt jemima_your aunt": "Family roles",
            # "94_mother nature_nature_nature is_mother": "Family roles",
            # "79_bagged_bagged that_that one_granddaughter": "Family roles",
            # "99_to me_my daughter_daughter_my granddaughter": "Family roles",

            # 3. Female names
            "6_karen_karen you_karen it_you karen": "Women names",
            "17_susan_susan susan_susan you_susan we": "Women names",
            "24_martha_martha you_martha martha_you martha": "Women names",
            # "46_helen_helen you_you helen_helen but": "Female names",
            # "54_linda_linda you_me linda_linda this": "Female names",
            # "55_carol_carol carol_christmas carol_carol they": "Female names",
            # "68_doris_irene_doris you_leaving": "Female names",
            # "71_her name_name_eve_name is": "Female names",
            # "77_margaret_you margaret_margaret margaret_atwood": "Female names",
            # "91_janet_janet it_and janet_you janet": "Female names",
            # "92_betty_crocker_betty crocker_barney": "Female names",
            # "23_alice_the moon_moon_moon alice": "Female names",
            # "64_mrs_butterworth_mrs butterworth_sisyphus": "Female names",
            # "61_dorothy_kansas_dorothy and_toto": "Female names",

            # 4. Food
            "18_cake_the cake_cake and_cake she": "Food",
            "9_feed_feed her_eat_to feed": "Food",
            "34_recipe_mother recipe_recipes_mom recipe": "Food",
            # "89_food_mom_midnight_snacking": "Food",
            "20_mustard_ketchup_low_low on": "Food",
            "15_fish_like fish_drink like_drink": "Food",
            "28_lemons_lemonade_you lemons_gives you": "Food",
            # "66_wine_blood_red_red wine": "Food",
            "37_grande_latte_venti_rio": "Food",
            # "69_vegan_vegetarian_she vegan_organic": "Food",

            # 5. Clothing, fashion & appearance
            "8_dress_fashion_wearing_wear": "Fashion & appearance",
            "35_shoes_shoe_her shoes_in shoe": "Fashion & appearance",
            # "78_hair_her hair_hair she_your hair": "Fashion & appearance",
            # "81_wear_wear this_dressed_dress": "Fashion & appearance",
            # "85_taller_smaller_look fat_height": "Fashion & appearance",
            # "90_lips_her lips_lip_red lips": "Fashion & appearance",
            # "59_collar_the collar_hot under_under the": "Fashion & appearance",
            # "98_ruff_ruff on_ruff she_the ruff": "Fashion & appearance",
            "33_neck_her neck_neck she_neck out": "Fashion & appearance",

            # 6. Animals
            "10_dog_her dog_pet_the dog": "Animals",
            "22_cat_cat lady_the cat_cats": "Animals",
            # "65_mosquitoes_mosquito_mosquitos_spray": "Animals",
            # "58_mouse_mice_rat_lab": "Animals",
            "12_peep_sheep_bo_bo peep": "Animals",

            # 7. Motherhood & parenting
            
            # "63_visit_to visit_your mother_visiting": "Motherhood",
            # "73_call_mother called_phone_call your": "Motherhood",

            # 8. Health, therapy & aging
            # "53_effects_side effects_acupuncture_viagra": "Health",
            # "84_therapist_therapy_my therapist_your therapist": "Health",
            # "72_diet_new diet_serious about_mom is": "Health",

            # 9. Work / finance / real estate
            # "48_college_mom_job_student": "Work",
            # "50_note_she left_left note_left": "Work",
            # "42_emails_her emails_email_server": "Work",

            # 10. Activities 
            # "82_book_books_read_author": "Activities",
            # "43_band_drummer_drum_beat": "Activities",

            # 11. Weather / seasons / nature ok
            "2_summer_the summer_this summer_fall": "Nature",
            "32_autumn_leaves_autumn leaves_the autumn": "Nature",
            "29_rose_rose garden_the rose_garden": "Nature",
            "19_stone_in stone_the stone_stone throw": "Nature",
            # "93_water_the water_for water_to water": "Nature",
            # "57_hudson_the hudson_hudson river_river": "Nature",
            # "67_parade_rain_her parade_rain on": "Nature",

            # 12. Mariage & Divorce ok
            "7_divorce_papers_divorce papers_the divorce": "Mariage",
            "27_in half_half_trick_her in": "Mariage",
            "4_trophy_trophy wife_your trophy_wife": "Mariage",
            "0_wife_my wife_your wife_ex": "Mariage",
            # "51_bride_the bride_you may_may now": "Mariage & Divorce",

            # 13. Climate
            "36_earth_mother earth_climate_climate change": "Climate",
            # 14. Fantasy / mythology ok
            "25_knight_armor_shining_in shining": "Fantasy & mythology",
            # "62_sword_the sword_her sword_scythe": "Fantasy & mythology",
            "21_witch_wicked witch_wicked_the witch": "Fantasy & mythology",
            "13_princess_the princess_castle_princess is": "Fantasy & mythology",
            "38_dragon_dragons_the dragon_of dragons": "Fantasy & mythology",

            # 15. COVID / pandemic ok
            # "41_quarantine_vaccine_covid_in quarantine": "COVID & pandemic",
            # "97_mask_masks_wear mask_wear": "COVID & pandemic",


            # 18. History ok
            # "44_neanderthal_dinosaurs_rex_dinosaur": "History",
            "31_stone age_age_the stone_stone": "History",

            # 19. Religion / morality ok
            # "74_grace_your grace_amazing grace_amazing": "Religion",
            # "76_faith_faith in_of faith_leap of": "Religion",

            # Money
            # "49_price_costco_the price_breaks": "Money",

            # House
            # "56_apartment_rent_realtor_the realtor": "House",
            # "96_moving_move_with us_moving back": "House",
            # "45_elevator_the elevator_stairs_hell": "House",

            # 20. Misc ok
            "26_bull_china_shop_china shop": "Miscellaneous",
            # "86_hiding_she hiding_the left_hiding something": "Miscellaneous",
            "39_madame_monsieur_et_and monsieur": "Miscellaneous",
            "30_size_matter_size doesn_doesn matter": "Miscellaneous",
            # "75_stepping stone_stepping_your stepping_stone": "Miscellaneous",
            "27_in half_half_trick_her in": "Miscellaneous",
            # "80_couch_this couch_sofa_the couch": "Miscellaneous",
            # "95_color_colors_true colors_true": "Miscellaneous", 
        }

        self.agg_topic_male_1 = {
            # Male archetypes
            "-1_don_he_to_the": "Men Archetypes", 
            "0_him_he_tell him_think he": "Men Archetypes", 
            "17_sir_arrived_brain_amazon": "Men Archetypes", 
            "35_last man_on earth_earth_man on": "Men Archetypes", 
            "39_men_man_male_man again": "Men Archetypes",
            "52_mob_villagers_sir_angry": "Men Archetypes",

            # Male names

            # Animals
            "16_whale_whale of_white whale_white": "Animals", 
            "10_cat_the cat_cats_leg": "Animals", 
            "20_bird_birds_the bird_pigeons": "Animals", 
            "33_mouse_mice_rat_the mice": "Animals", 
            "40_fish_tuna_fish out_of water": "Animals", 
            "51_elephant_elephant in_the elephant_the room": "Animals",

            # Climate

            # Clothing
            "27_shoes_boots_those_his shoes": "Fashion & appearance",

            # COVID / Pandemic

            # Death
            "6_penalty_death_death penalty_the death": "Death",

            # Family roles
            "54_brother_your brother_my brother_your": "Family roles",
            "5_dad_father_your father_your dad": "Family roles", 

            # Fantasy / mythology
            "14_damocles_sword_the sword_pen": "Fantasy & mythology",
            "30_peter_peter pan_pan_hoop": "Fantasy & mythology",
            

            # Money
            "21_stocks_stock_in stocks_stocks he": "Money", 

            # Food
            "12_dinner_for dinner_sir will_dinner sir": "Food", 
            "25_pizza_paparazzi_pizzarazzi_pepperoni": "Food", 
            "47_donut_doughnut_donuts_bagel": "Food",
            "50_beer_wine_drink_martini": "Food", 

            # Health
            "11_doctor_results_fraternity_mr": "Health", 
            "13_insurance_health_obamacare_care": "Health",

            # History
            "8_cave_man cave_man_his man": "History",

            # House
            "48_rent_house_housing_housebroken": "House", 
            "45_bathroom_the bathroom_toilet_the toilet": "House", 

            # Nature
            "23_plant_he plant_potted_potted plant": "Nature", 

            # Public Figures
            "22_hitchcock_mr hitchcock_alfred_alfred hitchcock": "Public Figures",

            # Politics
            "7_donald_trump_him donald_donald trump": "Politics",
            "9_voted_voted for_vote_for trump": "Politics",
            "19_wall_the wall_build_build wall": "Politics",
            "32_wave_trump wave_waves_trump": "Politics",

            # Pop culture
            "42_frank_stein_frank you_be frank": "Pop Culture",

            # Religion and Morality
            "1_pie_apple_adam_eve": "Religion",
            "43_sweater_moses_god_thou": "Religion",
            "46_george_george you_st george_george is": "Religion",
            "53_god_god is_god to_godot": "Religion",

            # Royal
            "2_king_the king_majesty_royal": "Royalty", 

            # Social
            "37_tweet_twitter_tweeting_tweets": "Social",

            # Work
            "26_boss_the boss_fired_re fired": "Work",
            "38_lawyers_lawyer_legal_case": "Work",
            "41_chairman_the chairman_chairman of_board": "Work",

            # Misc
            "3_don worry_worry_don_don know": "Miscellaneous",
            "4_reinventing_himself_invented_reinvent": "Miscellaneous",
            "15_yoga_mat_rug_carpet": "Miscellaneous",
            "18_size_bigger_matter_doesn matter": "Miscellaneous",
            "24_rock_rock and_roll_rock faster": "Miscellaneous",
            "28_sandbox_sand_the sandbox_desert": "Miscellaneous",
            "29_gravity_the gravity_gravity of_situation": "Miscellaneous",
            "31_wake_sleep_bed_nap": "Miscellaneous",
            "34_speed_you were_were going_the speed": "Miscellaneous",
            "36_printer_carl_3d_3d printer": "Miscellaneous",
            "44_shovel_snow_the shovel_son": "Miscellaneous",
            "49_cartoon_new yorker_yorker_caption": "Miscellaneous"

        }
    
        self.agg_topic_male_2 = {
            # Male archetypes
            "-1_don_the_he_you": "Men Archetypes", 
            "0_him_he_follow_us": "Men Archetypes",
            "53_men_men room_the men_room": "Men Archetypes",

            # Male names

            # Arts / Music
            "1_art_artist_work_his": "Arts & Music",
            "5_piano_piano man_the piano_play": "Arts & Music",

            # Animals
            "2_dog_park_the dog_sir": "Animals", 
            "21_fish_like fish_drink_drink like": "Animals", 
            "39_row_duck_ducks_quack": "Animals", 
            "52_cat_catnip_cats_pussy": "Animals",

            # Climate
            "8_global_global warming_warming_climate": "Climate", 

            # Clothing and Appearances
            "17_pants_wearing_pants he_clothes": "Fashion & appearance",
            "19_hair_bald_your hair_beard": "Fashion & appearance",
            "24_hands_big_big guy_the big": "Fashion & appearance",
            "37_high_he high_high don_looks high": "Fashion & appearance",
            "42_feet_his feet_foot_shoes": "Fashion & appearance",

            # COVID / Pandemic

            # Death
            "18_death_he died_died_killed": "Death",

            # Family roles
            "3_father_organ_steam_pipes": "Family roles", 
            "27_dad_father_your father_your dad": "Family roles", 

            # Fantasy / mythology
            "20_sword_the sword_desk_he who": "Fantasy & mythology",

            # Money
            "32_tax_taxes_tax returns_returns": "Money",
            "48_insurance_his insurance_the insurance_our insurance": "Money", 

            # Food
            "14_coffee_toast_wish_toaster": "Food", 
            "26_drink_beer_don drink_drink like": "Food", 
            "29_hot_hot dogs_dogs_hot dog": "Food", 
            "31_gingerbread_ginger_gingerbread man_the gingerbread": "Food", 
            "34_eat_eat him_to eat_feed him": "Food", 
            "43_menu_the menu_menu sir_sir": "Food", 
            "50_lunch_dinner_for dinner_for lunch": "Food",

            # Health

            # History
            "9_arthur_king arthur_king_arthur is": "History",
            "38_cave_man cave_the cave_cave man": "History",
            "49_dinosaurs_rex_dinosaur_the dinosaurs": "History",

            # House

            # Nature
            "16_seasonal_seasonal help_he seasonal_just seasonal": "Nature",
            "33_leaves_rake_leaf_tree": "Nature",

            # Public Figures
            "22_luther_martin_martin luther_messenger": "Public Figures",
            "41_putin_mueller_notes_russian": "Public Figures",

            # Politics
            "10_trump_donald_donald trump_president": "Politics",
            

            # Pop culture

            # Religion and Morality
            "12_god_of god_heaven_an act": "Religion",

            # Royal

            # Social
            "25_cable_channel_tv_netflix": "Social",
            "51_phone_cell_cell phone_app": "Social",

            # Sport
            "6_ball_bat_the ball_hit"
            "7_kite_kites_park_your kite"

            # Transport
            "15_train_model_trains_train set"
            "28_flight_fly_plane_flying"
            "46_uber_ride_driver_an uber"

            # Work
            "13_cop_good cop_bad cop_the good": "Work",

            # Misc
            "11_rock_rock and_between rock_and hard": "Miscellaneous",
            "4_don_look down_step_don worry": "Miscellaneous",
            "23_abominable_abominable he_him abominable_not abominable": "Miscellaneous",
            "30_swing_hits_hits it_world": "Miscellaneous",
            "35_galaxy_guide to_the galaxy_guide": "Miscellaneous",
            "36_clown_clowning_clowning around_bad clown": "Miscellaneous",
            "40_bite_teething_chew_don bite": "Miscellaneous",
            "44_table_round_round table_tables": "Miscellaneous",
            "45_won last_spring_last_be gone": "Miscellaneous",
            "47_frosty_customers_frosty he_the customers": "Miscellaneous",
            "48_selfie_camera_selfie with_mirror": "Miscellaneous",
            "54_amazon_we don_sir_don have": "Miscellaneous",


        }  
            
        self.agg_topic_male_3 = {
            # Male archetypes
            "51_boys_good boy_boy_the boys": "Men Archetypes",

            # Male names
            "43_harold_harold you_harold harold_harold it": "Men names", 

            # Arts / Music
            "41_singing_song_guitar_he singing": "Arts & Music",
            "48_jay_blues jay_blues_blue jay": "Arts & Music",

            # Animals
            "7_the king_horses_king horses_all the": "Animals", 
            "31_bird_birds_the birds_free bird": "Animals", 
            "34_bear_honey_honey bear_the bear": "Animals", 
            "37_salmon_the salmon_fresh_fish": "Animals", 
            "44_shark_sharks_the sharks_the shark": "Animals",
            "53_dog_dogs_the dogs_pet": "Animals",

            # Climate
            "39_climate_climate change_warming_global warming": "Climate",

            # Clothing and Appearances
            "3_tie_dress_jacket_pants": "Fashion & appearance",
            "22_hair_my hair_trim_haircut": "Fashion & appearance",
            "40_hat_scarf_hats_knit": "Fashion & appearance",
            "54_shoes_match_don match_heels": "Fashion & appearance",

            # COVID / Pandemic
            "35_virus_covid_coronavirus_covid 19": "COVID & pandemic",
            "50_social_distancing_social distancing_distance": "COVID & pandemic",
            "52_mask_masks_wearing mask_wear mask": "COVID & pandemic",

            # Death

            # Family roles
            "10_brother_big brother_big_your big": "Family roles",
            "12_father_dad_your father_my father": "Family roles",

            # Fantasy / mythology

            # Fatherhood
            

            # Money
            "33_rent_neighbor_downstairs_apartment": "Money",

            # Food
            "6_feed_feed him_him_eat": "Food", 
            "8_egg_nest egg_nest_an egg": "Food", 
            "9_drink_wine_red_glass": "Food", 
            "18_toast_sorry sir_sorry_toast sorry": "Food", 
            "20_rock_candy_rock candy_big rock": "Food", 
            "25_cheese_the cheese_cheese he_cheese don": "Food", 
            "28_gluten_gluten free_free_is gluten": "Food", 
            "29_burger_burger king_king_burgers": "Food", 

            # Health
            "17_effects_side effects_side_prescription": "Health",
            "30_diet_paleo_weight_carbs": "Health",
            "47_couch_lips_lip_therapy": "Health",

            # History

            # House

            # Mariage
            "21_cruise_viking_honeymoon_viking cruise": "Mariage",

            # Nature

            # Public Figures

            # Politics
            "32_wall_the wall_trump wall_trump": "Politics",

            # Pop culture
            "27_edward_scissorhands_edward scissorhands_movie": "Pop Culture",

            # Religion and Morality
            "26_george_flowers_st george_george is": "Religion",

            # Royal
            "5_king_the king_king of_be king": "Royalty",

            # Social
            "42_netflix_tv_password_account": "Social",

            # Sport
            "36_baseball_home run_pitch_home": "Sport",
            

            # Transport
            "23_clown_clowns_car_clown car": "Transport",
            "24_train_the train_subway_trains": "Transport",

            # Work
            "4_door_lane_officer_opened": "Work",
            "14_coffee_barista_jack_latte": "Work",
            "15_soup_my soup_waiter_waiter there": "Work",
            "16_work_job_home_from home": "Work",

            # Misc
            "11_disappear_court_contempt_magic": "Miscellaneous",
            "13_diversity_our_our new_new": "Miscellaneous",
            "19_weight_the weight_weight of_the world": "Miscellaneous",
            "38_parade_macy_balloon_thanksgiving": "Miscellaneous",
            "45_stand up_stand_up_first stand": "Miscellaneous",
            "46_hatch_hatching_to hatch_hatches": "Miscellaneous",
            "49_opponent_my opponent_world_flat": "Miscellaneous",

        }    

        self.agg_topic_male_4 = {
            # Male archetypes
            "-1_he_don_you_the": "Men Archetypes", 
            "21_good boy_boy_good_who good": "Men Archetypes", 
            "25_man_men_man who_like man": "Men Archetypes", 

            # Male names

            # Arts / Music
            "7_art_monet_sir_burgers": "Arts & Music",
            "46_roll_rock_and roll_rock and": "Arts & Music",

            # Animals
            "19_fish_the fish_fishes_seafood": "Animals", 
            "28_rabbit_the rabbit_hat_rabbit out": "Animals", 
            "31_lion_the lion_daniel_circus": "Animals", 
            "43_dog_the dog_dogs_son": "Animals", 
            "50_mosquitoes_mosquitos_bug_mosquito": "Animals",

            # Climate
            "27_climate_weather_climate change_the weather": "Climate", 

            # Clothing and Appearances
            "2_sheep_wool_clothing_sheep clothing": "Fashion & appearance",
            "5_suit_wear_dress_clothes": "Fashion & appearance",
            "11_mask_masks_wear_to wear": "Fashion & appearance",
            "40_shoes_shoe_shoes don_match": "Fashion & appearance",

            # COVID / Pandemic
            "37_covid_covid 19_19_virus": "COVID & pandemic",

            # Death

            # Family roles
            "18_brother_your brother_your_little brother": "Family roles",
            "6_father_dad_your father_your dad": "Family roles",

            # Fantasy / mythology
            "36_moon_the moon_man in_the man": "Fantasy & mythology",
            
            # Money
            "48_insurance_his insurance_the insurance_our insurance": "Money",

            # Food And Drinks
            "3_lemonade_lemons_make lemonade_you lemons": "Food", 
            "15_rat_lab_mouse_mice": "Food", 
            "22_mustard_ketchup_relish_jackson": "Food", 
            "24_wine_drink_for drink_drinking": "Food", 
            "32_dinner_eat_lunch_ate": "Food", 
            "41_apple_an apple_dad_the apple": "Food", 


            # Health

            # History
            "17_cave_man cave_man_your man": "History",

            # House
            "12_piano_the house_house_house down": "House", 
            "16_water_boss_clean_shower": "House", 
            "47_houses_house_flipping_flip": "House", 

            # Mariage
            "34_cake_groom_down cake_the cake": "Mariage",

            # Nature
            "13_rock_the rock_rocks_rock and": "Nature",
            "42_leaves_leaf_the leaves_rake": "Nature",

            # Public Figures
            "44_george_karma_boy george_martin": "Public Figures",

            # Politics
            "4_trump_donald_election_vote": "Politics",

            # Pop culture
            "0_jack_cloud_bean_beans": "Pop Culture",
            "8_pet_boys_beach_beach boys": "Pop Culture",

            # Religion and Morality

            # Royal
            "49_king_throne_kings_the king": "Royalty",

            # Social

            # Sport

            # Transport

            # Work
            "1_your honor_honor_witness_bear": "Work",
            "23_salesman_sales_our best_best": "Work",
            "45_hired_hire_hired him_job": "Work",
            "51_chef_the chef_special_our chef": "Work",
            "52_school_in school_stay in_stay": "Work",

            # Misc
            "9_book_books_author_read": "Miscellaneous",
            "10_city_the city_he ll_pace": "Miscellaneous",
            "14_square_round_hole_peg": "Miscellaneous",
            "20_don worry_worry_don_worry we": "Miscellaneous",
            "26_china_china shop_shop_china he": "Miscellaneous",
            "29_feel_don feel_feel seen_don see": "Miscellaneous",
            "30_upside_upside down_down_world": "Miscellaneous",
            "33_bite_don bite_males_bite don": "Miscellaneous",
            "35_friendly_nice_he nice_he friendly": "Miscellaneous",
            "38_ignore him_ignore_attention_just ignore": "Miscellaneous",
            "39_bubble_burst_your bubble_burst your": "Miscellaneous",
            "53_them_valuable_they must_must be": "Miscellaneous",
            "54_gravity_the gravity_gravity of_situation": "Miscellaneous"
        }
    
        # Female themes
        self.theme_words_female = {
            "Women archetypes": ["women", "woman", "female", "girls"],
            "Politics": ["Hillary", "voted"],
            "Royalty": ["queen", "majesty"],
            "Family roles": ["mother", "mom", "sister", "grandma", "grandmother"],
            "Women names": ["Karen", "Susan", "Martha"],
            "Food": ["cake", "feed", "eat", "recipe", "mother recipe", "mustard", "ketchup", "fish", "lemons", "lemonade", "latte"],
            "Fashion & appearance": ["dress", "fashion", "wearing", "shoes", "neck"],
            "Animals": ["dog", "cat", "lady cat"],
            "Nature": ["summer", "autumn", "leaves", "rose", "garden", "stone"],
            "Mariage": ["divorce", "trophy wife", "wife", "ex wife", "divorce papers"],
            "Climate": ["earth", "climate change", "climate"],
            "Fantasy & mythology": ["knight", "witch", "princess", "castle", "dragons"],
            "History": ["stone age"],
            "Miscellaneous": ["china", "size", "half", "bull"]
        }

        # Male themes
        self.theme_words_male = {
            "Men Archetypes": ["he", "him", "sir", "men", "male", "man", "boys"],
            "Men names": ["Harold"],
            "Animals": ["whale", "cat", "lion", "mosquito", "rabbit", "horse", "bear", "salmon", "shark", "bird", "pigeons", "mouse", "fish", "elephant", "dog", "duck"],
            "Arts & Music": ["art", "artist", "piano", "sing", "guitar", "Jay Blues", "Monet"],
            "Climate": ["climate", "global waring", "change"],
            "COVID & pandemic": ["virus", "covid", "coronavirus", "covid 19", "social distancing", "masks"],
            "Fashion & appearance": ["tie", "jackets", "hair", "hat", "shoes", "boots", "pants", "wearing", "hair", "bald", "hands", "big guy", "feet"],
            "Death": ["death", "death penalty", "died", "killed"],
            "Family roles": ["brother", "dad", "father"],
            "Fantasy & mythology": ["damocles sowrd", "peter pan", "sword"],
            "Mariage": ["honeymoon", "groom"],
            "Money": ["stocks", "tax", "insurance", "rent"],
            "Food": ["dinner", "burger", "pizza", "donut", "beer", "wine", "martini", "coffe", "eat", "gingerbread", "menu", "lunch dinner"],
            "Health": ["doctor", "insurance", "health", "obamacare"],
            "History": ["cave man", "king Arthur", "dinosaurs"],
            "House": ["bathroom", "housing", "house shower"],
            "Nature": ["plant", "potted", "seasonal", "leaves", "rock"],
            "Public Figures": ["Alfred Hitchcock", "Martin Luther", "Putin", "George Martin"],
            "Politics": ["Donald Trump", "Trump", "build wall", "voted", "president", "election"],
            "Pop Culture": ["Frankenstein", "Edward scissorhands"],
            "Religion": ["adam", "eve", "apple", "god", "St-George", "heaven"],
            "Royalty": ["king", "majesty", "throne"],
            "Social": ["tweet", "twitter", "netflix", "phone"],
            "Sport": ["ball", "bat", "kite", "baseball", "pitch"],
            "Transport": ["train", "fly", "plane", "uber", "subway"],
            "Work": ["salesman", "chef", "boss", "fired", "lawyers", "chairman", "cop", "officer", "waiterm job"],
            "Miscellaneous": ["bigger", "mat", "reinventing", "worry", "speed", "printer", "shovel", "galaxy", "table", "camera"]
        }
   
        self.theme_colors_female = {
            "Women archetypes": "#FFB3BA",      # soft pink
            "Politics": "#BAE1FF",               # light blue
            "Royalty": "#FFFBAE",                # pale yellow
            "Family roles": "#BAFFC9",           # mint green
            "Women names": "#FFDFBA",           # peach
            "Food": "#FFB3FF",                   # pastel magenta
            "Fashion & appearance": "#D5BAFF",   # lavender
            "Animals": "#8FB9D8",                # light blue
            "Nature": "#9CF4C4",                  # pale green
            "Mariage": "#FFBABA",                # soft coral
            "Climate": "#FFFFBA",                # pastel yellow
            "Fantasy & mythology": "#FFC2F2",    # soft pink-lavender
            "History": "#BEDDF4",                # light blue
            "Miscellaneous": "#E0BAFF"           # light purple
            }

        self.theme_colors_male = {
            # Common themes with female palette
            "Animals": self.theme_colors_female["Animals"],
            "Climate": self.theme_colors_female["Climate"],
            "Fashion & appearance": self.theme_colors_female["Fashion & appearance"],
            "Family roles": self.theme_colors_female["Family roles"],
            "Fantasy & mythology": self.theme_colors_female["Fantasy & mythology"],
            "Mariage": self.theme_colors_female["Mariage"],
            "Nature": self.theme_colors_female["Nature"],
            "Food": self.theme_colors_female["Food"],
            "History": self.theme_colors_female["History"],
            "Politics": self.theme_colors_female["Politics"],
            "Royalty": self.theme_colors_female["Royalty"],
            "Miscellaneous": self.theme_colors_female["Miscellaneous"],

            # Male-specific themes (new pastel colors)
            "Men Archetypes": "#FFA07A",       # light salmon
            "Men names": "#FFDAB9",            # peach puff
            "Arts & Music": "#B0E0E6",          # powder blue
            "COVID & pandemic": "#E6E6FA",      # lavender
            "Death": "#F5DEB3",                 # wheat
            "Money": "#FFE4B5",                  # moccasin
            "Health": "#C1FFC1",                 # light green
            "House": "#F0E68C",                  # khaki
            "Public Figures": "#D8BFD8",         # thistle
            "Pop Culture": "#E0FFFF",            # light cyan
            "Religion": "#F0FFF0",               # honeydew
            "Social": "#FFEFD5",                 # papaya whip
            "Sport": "#FAFAD2",                  # light goldenrod yellow
            "Transport": "#F5F5DC",              # beige
            "Work": "#FFFACD"                    # lemon chiffon
        }

    
    # ---------------------------
    # PART 1 – GENDER DETECTION
    # ---------------------------

    def get_metadata(self, dataC):
        """
        Preps the metadata to be utilized in the analysis
        """

        dataC0 = dataC.copy(deep = True)

        # put it in lower case
        dataC0["image_descriptions"] = dataC0["image_descriptions"].apply(
            lambda x: [s.lower() for s in x] if isinstance(x, list) else str(x).lower()
        )
        # remove the []
        dataC0["image_descriptions"] = dataC0["image_descriptions"].apply(
            lambda x: " ".join(x) if isinstance(x, list) else str(x)
        )
        dataC0['gender_mention'] = dataC0['image_descriptions'].apply(self.detect_gender)

        return dataC0
    
    def detect_gender_vectorized(self, df: pd.DataFrame) -> pd.Series:

        # Vectorized detection using compiled regex (runs in C)
        male_hits = df["caption"].str.contains(self.male_regex, na=False)
        female_hits = df["caption"].str.contains(self.female_regex, na=False)

        # Build result column
        result = pd.Series("neutral", index=df.index)
        result[male_hits & female_hits] = "both"
        result[male_hits & ~female_hits] = "male"
        result[female_hits & ~male_hits] = "female"

        return result

    def get_Top_captions(self, dataA, num = np.inf):
        
        dataTop10 = []
        # count = []

        for idx in range(len(dataA)):

            contest = dataA[idx]

            # Keep only the top num rows
            df_top = contest[contest.index < num].copy()

            # Convert caption column to clean lowercase strings
            df_top["caption"] = (
                df_top["caption"]
                .astype(str)    # handles lists or other types
                .str.lower()
            )

            # Apply fast vectorized gender classifier
            df_top["gender_mention"] = self.detect_gender_vectorized(df_top)

            dataTop10.append(df_top)

            # # Count mentions per contest
            # gender_counts = (
            #     df_top10["gender_mention"]
            #     .value_counts()
            #     #.unstack(fill_value=0)
            #     .reset_index()
            # )

            # count.append(gender_counts)

        return dataTop10 # count,

    def detect_gender(self, text: str) -> str:
        """
        Detects whether a text mentions male, female, both, or neutral terms.
        Returns one of: "male", "female", "both", or "neutral".
        """

        male = any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in self.male_terms)
        female = any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in self.female_terms)

        if male and female:
            return "both"
        elif male:
            return "male"
        elif female:
            return "female"
        else:
            return "neutral"
        
    def distribution_captions(self, count):

        # Overall distribution of gender over all the top captions.

        # Combine all contests
        combined = []
        for i, df in enumerate(count):
            temp = df.copy()
            temp["contest_index"] = i + 1  # add contest number
            combined.append(temp)

        all_count = pd.concat(combined, ignore_index=True)
        pivoted = (
            all_count.pivot(index="contest_index", columns="gender_mention", values="count")
            .fillna(0)
            .sort_index()
        )

        overall_counts = (
            all_count.groupby("gender_mention")["count"]
            .sum()
            .sort_values(ascending=False)
        )

        return overall_counts, pivoted

    # ---------------------------
    # PART 2 – WORDS ANALYSIS
    # ---------------------------   
    @staticmethod
    def is_it_proper(word: str, proper_nouns: Dict[str, Dict[str, int]]) -> None:
        """
        Identifies proper nouns (capitalized words) and counts their occurrences
        in a dictionary structured as:
        {word_lower: {'upper': count, 'lower': count}}
        """

        case = 'upper' if word[0].isupper() else 'lower'
        word_lower = word.lower()

        if word_lower not in proper_nouns:
            proper_nouns[word_lower] = {case: 1}
        else:
            proper_nouns[word_lower][case] = proper_nouns[word_lower].get(case, 0) + 1

    @staticmethod
    def gender_the_sentence(sentence_words: Set[str],
                            male_words: Set[str],
                            female_words: Set[str]) -> str:
        """
        Returns the gender associated with a sentence based on overlap with gendered word lists.
        """

        mw_length = len(male_words.intersection(sentence_words))
        fw_length = len(female_words.intersection(sentence_words))

        if mw_length > 0 and fw_length == 0:
            return 'male'
        elif mw_length == 0 and fw_length > 0:
            return 'female'
        elif mw_length > 0 and fw_length > 0:
            return 'both'
        else:
            return 'none'

    @staticmethod
    def increment_gender(sentence_words: List[str],
                         gender: str,
                         sentence_counter: Dict[str, int],
                         word_counter: Dict[str, int],
                         word_freq: Dict[str, Dict[str, int]]) -> None:
        """
        Updates counters for sentences, words, and word frequencies by gender.
        """

        sentence_counter[gender] = sentence_counter.get(gender, 0) + 1
        word_counter[gender] = word_counter.get(gender, 0) + len(sentence_words)

        if gender not in word_freq:
            word_freq[gender] = {}

        for word in sentence_words:
            word_freq[gender][word] = word_freq[gender].get(word, 0) + 1

    def analyse_text(self, 
                     data, 
                     tokenizer, 
                     punctuation, 
                     sentence_counter, 
                     word_counter, 
                     word_freq, 
                     proper_nouns, 
                     C: bool = False) -> None:
        """
        Analyzes text data in a pandas DataFrame to detect gendered terms and 
        update sentence and word frequency counters.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing text columns ('caption' or 'image_descriptions').
        tokenizer : object
            A sentence tokenizer (e.g. nltk.data.load('tokenizers/punkt/english.pickle')).
        punctuation : str
            String of punctuation characters to strip (e.g. string.punctuation).
        sentence_counter : dict
            Dictionary tracking the number of sentences per gender.
        word_counter : dict
            Dictionary tracking the number of words per gender.
        word_freq : dict
            Dictionary tracking frequency of words per gender.
        proper_nouns : dict
            Dictionary tracking proper noun capitalization patterns.
        C : bool, optional
            If True, analyze 'image_descriptions'; otherwise, analyze 'caption'.
        """

        column = 'image_descriptions' if C else 'caption'
        list_text = data[column].values

        for idx in range(data.shape[0]):
            text = list_text[idx]

            # Split into sentences
            sentences = tokenizer.tokenize(text)

            for sentence in sentences:
                # Word tokenize and strip punctuation
                sentence_words = sentence.split()
                sentence_words = [
                    w.strip(punctuation) for w in sentence_words 
                    if len(w.strip(punctuation)) > 0
                ]

                # Track capitalization for proper nouns
                for word in sentence_words[1:]:
                    self.is_it_proper(word, proper_nouns)

                # Lowercase and deduplicate words
                sentence_words = set(w.lower() for w in sentence_words)

                # Determine gender of the sentence
                gender = self.gender_the_sentence(
                    sentence_words, 
                    set(self.male_terms), 
                    set(self.female_terms)
                )

                # Increment counters
                self.increment_gender(sentence_words, gender, sentence_counter, word_counter, word_freq)

    # ---------------------------
    # PART 3 – TOPIC MODELLING
    # ---------------------------

    @staticmethod
    def map_topic(topic_caption, agg_topic):

        # Convert keys like "3_women_woman..." into int IDs
        agg_topic_int = {
            int(key.split("_")[0]): value
            for key, value in agg_topic.items()
        }
        
        df_topics = pd.DataFrame({
        "caption": topic_caption['caption'].values,
        "topic": topic_caption['topic'].values
        })
        df_topics["aggregated_theme"] = df_topics["topic"].map(agg_topic_int)
        df_topics = df_topics.sort_values('topic')
        df_topics = df_topics.dropna(subset=["aggregated_theme"])

        return df_topics
    
    def lighten_color(self, hex_color, factor=0.5):
        """
        Lighten the given hex color by a factor (0 = black, 1 = original color)
        """
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Linear interpolation to white
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        return f"#{r:02X}{g:02X}{b:02X}"

    def plot_topic(self, df_topics, gender, theme_keywords, theme_colors):

        if gender == 'male':
            gender_ = 'men'
        else: 
            gender_ = 'women'
        
        # Standardize theme names
        df_topics["aggregated_theme"] = df_topics["aggregated_theme"].str.strip()

        # Count themes
        theme_counts = df_topics["aggregated_theme"].value_counts().sort_values(ascending=False)
        total_captions = theme_counts.sum()
        theme_percent = (theme_counts / total_captions) * 100

        circle_data = []

        for theme in theme_counts.index:
            theme_size = theme_counts[theme]

            # Top-level theme
            circle_data.append(dict(
                id=theme,
                parent="",
                value=theme_size,
                type="theme",
                percent=theme_percent[theme]
            ))

            # # Child nodes: only if theme exists in keywords
            words = theme_keywords.get(theme, [])
            # Assign larger values to words
            word_value = max(theme_size / len(words), 1)*2  # ensures visible
            for word in words[:20]:  # max 20 words
                circle_data.append(dict(
                    id=word,
                    parent=theme,  # must exactly match top-level theme id
                    value=word_value,
                    type="word", 
                    percent = None  # maybe remove
                ))

        df_circles = pd.DataFrame(circle_data)

        # Create a new column in df_circles for coloring
        df_circles["color_hex"] = df_circles.apply(
            lambda row: theme_colors[row["id"]] if row["type"]=="theme" 
                        else self.lighten_color(theme_colors[row["parent"]], factor=0.5),
            axis=1
        )
        color_map = {row["id"]: row["color_hex"] for idx, row in df_circles.iterrows()}

        fig = px.treemap(
            df_circles,
            names="id",
            parents="parent",
            values="value",
            color="id",  # use id as key
            color_discrete_map=color_map, 
            title=f"Themes in {gender_} labeled captions",
            custom_data=["percent", "type"]
        )
        # Create a hover_text column
        df_circles["hover_text"] = df_circles.apply(
            lambda row: f"<b>{row['id']}</b><br>Count: {row['value']}<br>Perc: {row['percent']:.2f}%" 
                        if row["type"] == "theme"  # Show count and percentage for themes
                        else f"<b>{row['parent']}",  # For words, just show parent
            axis=1
        )
        fig.update_traces(root_color="lightgrey")
        # Use precomputed hover text
        fig.update_traces(hovertemplate="%{customdata}<extra></extra>", customdata=df_circles["hover_text"])

        fig.show()

        return fig

    # ---------------------------
    # PART 4 - FUNNY SCORE
    # ---------------------------

    def get_stats_funny_score(self, data_caption, plot_distrib = False, plot_evolution = False):

        mean_funny_female = []
        std_funny_female = []
        list_funny_female = []

        mean_funny_male = []
        std_funny_male = []
        list_funny_male = []

        for contest in data_caption:
            fem = contest[contest['gender_mention'] == 'female']
            mean_funny_female.append(fem['funny_score_scaled'].mean())
            std_funny_female.append(fem['funny_score_scaled'].std())
            list_funny_female.append(fem['funny_score_scaled'].values)
            male = contest[contest['gender_mention'] == 'male']
            mean_funny_male.append(male['funny_score_scaled'].mean())
            std_funny_male.append(male['funny_score_scaled'].std())
            list_funny_male.append(male['funny_score_scaled'].values)

        if plot_distrib:

            flatten_funny_male = self.flatten(list_funny_male)
            flatten_funny_female = self.flatten(list_funny_female)

            # Colorblind-friendly colors
            MEN_COLOR = "#0072B2"
            WOMEN_COLOR = "#D55E00"

            fig = go.Figure()

            # Women histogram
            fig.add_trace(go.Histogram(
                x=flatten_funny_female,
                name="Women",
                histnorm="probability density",
                opacity=0.5,
                marker_color=WOMEN_COLOR
            ))

            # Men histogram
            fig.add_trace(go.Histogram(
                x=flatten_funny_male,
                name="Men",
                histnorm="probability density",
                opacity=0.5,
                marker_color=MEN_COLOR
            ))

            # Layout
            fig.update_layout(
                title="Funniness Distribution by Gender",
                xaxis_title="Funny Score",
                yaxis_title="Density",
                barmode="overlay",
                template="plotly_white",
                hovermode="x unified",
                legend=dict(
                    orientation="h",  # horizontal
                    yanchor="bottom",
                    y=1.02,           # slightly above the plot
                    xanchor="center",
                    x=0.5)
            )

            fig.show()
            fig.write_html("funniness_distrib_by_gender.html")

        if plot_evolution:

            # Colorblind-friendly colors
            MEN_COLOR = "rgba(0,114,178,1)"       # solid line
            MEN_FILL = "rgba(0,114,178,0.2)"      # semi-transparent fill
            WOMEN_COLOR = "rgba(213,94,0,1)"      # solid line
            WOMEN_FILL = "rgba(213,94,0,0.2)"     # semi-transparent fill

            # X values
            x_female = np.linspace(0, len(mean_funny_female), len(mean_funny_female)+1)[1:]
            x_male = np.linspace(0, len(mean_funny_male), len(mean_funny_male)+1)[1:]

            fig = go.Figure()

            # Women shaded area (mean ± std)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_female, x_female[::-1]]),
                y=np.concatenate([
                    np.array(mean_funny_female) + np.array(std_funny_female),
                    (np.array(mean_funny_female) - np.array(std_funny_female))[::-1]
                ]),
                fill='toself',
                fillcolor=WOMEN_FILL,
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                name="Women",
                legendgroup="women",
                showlegend=True
            ))

            # Women mean line
            fig.add_trace(go.Scatter(
                x=x_female,
                y=mean_funny_female,
                mode='lines+markers',
                name="Women",
                legendgroup="women",
                showlegend=False,  # important: only one legend entry
                line=dict(color=WOMEN_COLOR, width=2),
                marker=dict(size=2)
            ))


            # Men shaded area (mean ± std)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_male, x_male[::-1]]),
                y=np.concatenate([
                    np.array(mean_funny_male) + np.array(std_funny_male),
                    (np.array(mean_funny_male) - np.array(std_funny_male))[::-1]
                ]),
                fill='toself',
                fillcolor=MEN_FILL,
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                name="Men",
                legendgroup="men",
                showlegend=True
            ))

            # Men mean line
            fig.add_trace(go.Scatter(
                x=x_male,
                y=mean_funny_male,
                mode='lines+markers',
                name="Men",
                legendgroup="men",
                showlegend=False,  # important
                line=dict(color=MEN_COLOR, width=2),
                marker=dict(size=2)
            ))


            # Layout
            fig.update_layout(
                title="Evolution of the Funny Score by Gender",
                xaxis_title="Contest",
                yaxis_title="Funny Score",
                xaxis=dict(range=[0, 240]),
                template="plotly_white",
                hovermode="x unified",
                width=1000,
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    groupclick="togglegroup"  
                )
            )

            fig.show()
            fig.write_html("evolution_funny_score.html")
        
    def flatten(self, lst):
        flattened_list = []
        for i in lst:
            reshaped = i.reshape(-1).tolist()
            flattened_list.extend(reshaped)
        return flattened_list

    def cliffs_delta(self, x, y):
        """
        Compute Cliff's delta effect size.
        Returns value in [-1, 1].
        """
        x = np.asarray(x)
        y = np.asarray(y)

        n_x = len(x)
        n_y = len(y)

        greater = 0
        lower = 0

        for xi in x:
            greater += np.sum(xi > y)
            lower += np.sum(xi < y)

        return (greater - lower) / (n_x * n_y)

    def split_top_bottom(self, df, score_col="funny_score_scaled", q=0.10):
        """
        Splits a dataframe into top and bottom q percent based on a score column.
        """
        lower_thresh = df[score_col].quantile(q)
        upper_thresh = df[score_col].quantile(1 - q)

        bottom = df[df[score_col] <= lower_thresh].copy()
        top = df[df[score_col] >= upper_thresh].copy()

        return top, bottom
    
    def compute_stats(self, x, y):
        u_stat, p_value = mannwhitneyu(x, y, alternative="two-sided")
        delta = self.cliffs_delta(x, y)
        print("Mann-Whitney U:", u_stat)
        print("p-value:", p_value)
        print(f"Cliff's delta: {delta:.3f}")
        return u_stat, p_value, delta
    # ---------------------------
    # VISUALIZATION
    # ---------------------------

    @staticmethod
    def plot_overall_counts(
        overall_counts,
        title: str = "Overall Presence of Gender Mentions",
        xlabel: str = "Gender Mention Category",
        ylabel: str = "Number of Captions",
        colors: str = "skyblue",
        edgecolor: str = "black",
        neutral: bool = True
    ):
        """
        Plots a bar chart showing the overall presence of gender mentions.

        Parameters
        ----------
        overall_counts : pd.DataFrame or pd.Series
            Must contain columns or index for ['male', 'female', 'both'].
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        colors : str or list, optional
            Color(s) for bars.
        edgecolor : str, optional
            Edge color for bars.
        """
        if neutral:
            plt.figure(figsize=(6, 4))
            overall_counts[["male", "female", "both", "neutral"]].plot(
                kind='bar', color=colors, edgecolor=edgecolor
            )
        else: 
            plt.figure(figsize=(6, 4))
            overall_counts[["male", "female", "both"]].plot(
                kind='bar', color=colors, edgecolor=edgecolor
            )

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_cumulative_mentions(
        cumulative,
        title: str = "Cumulative Gender Mentions per Contest",
        xlabel: str = "Contest Index (chronological)",
        ylabel: str = "Cumulative Count",
        legend_title: str = "Gender Mention",
        neutral: bool = True
    ):
        """
        Plots the cumulative count of gender mentions across contests.

        Parameters
        ----------
        cumulative : pd.DataFrame
            A dataframe where each column corresponds to a gender category,
            and the index represents contest order.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        legend_title : str, optional
            Title for the legend.
        """
        plt.figure(figsize=(10, 6))

        if neutral:
            for col in cumulative.columns:
                plt.plot(cumulative.index, cumulative[col], label=col, linewidth=2)
        else: 
            for col in cumulative.columns[:-1]:
                plt.plot(cumulative.index, cumulative[col], label=col, linewidth=2)
                
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(title=legend_title)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_gender_cooccurrence(
        cross,
        title: str = "Gender Co-occurrence: Image vs Caption",
        xlabel: str = "Caption Gender",
        ylabel: str = "Image Gender",
        cmap: str = "Blues"
    ):
        """
        Plots a heatmap of gender co-occurrence between image and caption.

        Parameters
        ----------
        cross : pd.DataFrame
            Cross-tabulation of gender categories for image vs caption.
        title : str, optional
            Plot title.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        cmap : str, optional
            Color map for heatmap.
        """
        plt.figure(figsize=(6, 5))
        sns.heatmap(cross, annot=True, fmt="d", cmap=cmap, cbar=False)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_wordclouds(male_cloud, female_cloud, word_type):
        """
        Displays male and female word clouds side by side.

        Parameters
        ----------
        male_cloud : wordcloud.WordCloud
            Word cloud object for male-dominant words.
        female_cloud : wordcloud.WordCloud
            Word cloud object for female-dominant words.
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))

        axes[0].imshow(male_cloud, interpolation='bilinear')
        axes[0].set_title(f'Top {word_type} associated with men', fontsize=16)
        axes[0].axis('off')

        axes[1].imshow(female_cloud, interpolation='bilinear')
        axes[1].set_title(f'Top {word_type} associated with women', fontsize=16)
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_cumulative_mentions_plotly(
        cumulative,
        title: str = "Cumulative Gender Mentions per Contest",
        xlabel: str = "Contest Index (chronological)",
        ylabel: str = "Cumulative Count",
        legend_title: str = "Gender Mention",
        neutral: bool = True, 
        save: str = None
    ):
        """
        Interactive Plotly version of cumulative gender mentions.
        """

        fig = go.Figure()

        # --- Label mapping ---
        label_map = {
            "male": "men",
            "female": "women",
            "both": "both",
            "neutral": "neutral"
        }

        columns = cumulative.columns if neutral else cumulative.columns[:-1]

        for col in columns:
            display_name = label_map.get(col, col)
            fig.add_trace(
                go.Scatter(
                    x=cumulative.index,
                    y=cumulative[col],
                    mode="lines",
                    name=display_name,
                    line=dict(width=3),
                    hovertemplate=(
                        f"<b>{col}</b><br>"
                        "Contest: %{x}<br>"
                        "Count: %{y}<extra></extra>"
                    )
                )
            )

        fig.update_layout(
            title=dict(text=title, x=0.5),
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            legend_title=legend_title,
            template="plotly_white",
            hovermode="x unified",
            width=900,
            height=500
        )

        fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")

        if save: 
            fig.write_html(save)

        fig.show()

    @staticmethod
    def plot_overall_counts_plotly(
        overall_counts,
        title: str = "Overall Presence of Gender Mentions",
        xlabel: str = "Gender Mention Category",
        ylabel: str = "Number of Captions",
        neutral: bool = True, 
        save: str = None
    ):
        """
        Interactive Plotly version of overall gender mention counts.
        """

        categories = ["male", "female", "both", "neutral"] if neutral else ["male", "female", "both"]
        values = overall_counts[categories]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=categories,
                    y=values,
                    text=values,
                    textposition="auto",
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Count: %{y}<extra></extra>"
                    )
                )
            ]
        )

        # --- Label mapping ---
        label_map = {
            "male": "men",
            "female": "women",
            "both": "both",
            "neutral": "neutral"
        }

        fig.update_layout(
            title=dict(text=title, x=0.5),
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            template="plotly_white",
            width=600,
            height=450
        )

        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
        # --- Change only displayed tick labels ---
        fig.update_xaxes(
            tickvals=categories,
            ticktext=[label_map[c] for c in categories],
            tickangle=0
    )


        if save: 
            fig.write_html(save)

        fig.show()

    @staticmethod
    def plot_average_sentiment_by_theme_plotly(
        df_common,
        title: str = "Average Sentiment by Theme (Common Themes Only)",
        xlabel: str = "Theme",
        ylabel: str = "Average Sentiment",
        pos_threshold: float = 0.05,
        neg_threshold: float = -0.05, 
        save: str = None
    ):
        """
        Plot mean sentiment per theme and gender with 95% CI.
        """

        # --- Aggregate: mean, std, count ---
        summary = (
            df_common
            .groupby(["aggregated_theme", "gender_label"])
            .agg(
                mean_sentiment=("sentiment", "mean"),
                std_sentiment=("sentiment", "std"),
                n=("sentiment", "count")
            )
            .reset_index()
        )

        # --- 95% confidence interval ---
        summary["ci"] = 1.96 * summary["std_sentiment"] / np.sqrt(summary["n"])

        # --- Build figure ---
        fig = go.Figure()

        for gender in summary["gender_label"].unique():
            df_g = summary[summary["gender_label"] == gender]

            fig.add_trace(
                go.Bar(
                    x=df_g["aggregated_theme"],
                    y=df_g["mean_sentiment"],
                    name=gender,
                    error_y=dict(
                        type="data",
                        array=df_g["ci"],
                        visible=True
                    ),
                    hovertemplate=(
                        "<b>Theme:</b> %{x}<br>"
                        f"<b>Gender:</b> {gender}<br>"
                        "<b>Mean sentiment:</b> %{y:.3f}<br>"
                        "<b>95% CI:</b> ±%{error_y.array:.3f}"
                        "<extra></extra>"
                    )
                )
            )

        # --- Sentiment threshold lines ---
        fig.add_hline(
            y=pos_threshold,
            line_dash="dot",
            line_color="green"
        )

        fig.add_hline(
            y=neg_threshold,
            line_dash="dot",
            line_color="red"
        )

        # --- Neutral zone shading ---
        fig.add_hrect(
            y0=neg_threshold,
            y1=pos_threshold,
            fillcolor="gray",
            opacity=0.12,
            line_width=0
        )

        # --- Layout ---
        fig.update_layout(
            title=dict(text=title, x=0.5),
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            barmode="group",
            template="plotly_white",
            width=1300,
            height=600,
            legend_title="Gender",
            hovermode="closest"
        )

        fig.update_xaxes(tickangle=90)
        fig.update_yaxes(
            zeroline=True,
            zerolinecolor="black",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        )

        fig.show()

    @staticmethod
    def plot_5_percent_distrib_plotly(men_bottom, men_top, women_bottom, women_top, q):
        
        # Colorblind-friendly colors
        MEN_COLOR = "#0072B2"
        WOMEN_COLOR = "#D55E00"
        
        fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Worst Captions", "Top Captions"),
        shared_yaxes=True
        )

        # Worst captions
        fig.add_trace(go.Histogram(
            x=men_bottom["funny_score_scaled"],
            name="Men",
            histnorm="probability density",
            opacity=0.4,
            marker_color=MEN_COLOR,
            showlegend=False  # avoid duplicate legend entries
        ), row=1, col=1)

        fig.add_trace(go.Histogram(
            x=women_bottom["funny_score_scaled"],
            name="Women",
            histnorm="probability density",
            opacity=0.4,
            marker_color=WOMEN_COLOR,
            showlegend=False
        ), row=1, col=1)

        # Top captions
        fig.add_trace(go.Histogram(
            x=men_top["funny_score_scaled"],
            name="Men",
            histnorm="probability density",
            opacity=0.4,
            marker_color=MEN_COLOR
        ), row=1, col=2)

        fig.add_trace(go.Histogram(
            x=women_top["funny_score_scaled"],
            name="Women",
            histnorm="probability density",
            opacity=0.4,
            marker_color=WOMEN_COLOR
        ), row=1, col=2)

        fig.update_layout(
            title=f"Funny Score Distribution by Gender ({int(q*100)}%)",
            barmode="overlay",
            template="plotly_white",
            hovermode="x unified"
        )

        fig.update_xaxes(title_text="Funny score")
        fig.update_yaxes(title_text="Density")

        fig.show()

        fig.write_html("funny_score_distrib_5.html")

    # ---------------------------
    # LOADING FILES
    # ---------------------------
    @staticmethod
    def load_pickle(path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        return data

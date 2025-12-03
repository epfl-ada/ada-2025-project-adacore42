import re
from typing import List, Set, Dict


class GenderAnalysis:
    """
    A class grouping utility functions for detecting and analyzing gendered language in text.
    """

    def __init__(self):
        # Word lists from Danielle Sucher's "Jailbreak the Patriarchy"
        self.male_terms = [
            'guy', 'spokesman', 'chairman', "men's", 'men', 'him', "he's", 'his', 'boy',
            'boyfriend', 'boyfriends', 'boys', 'brother', 'brothers', 'dad', 'dads',
            'dude', 'father', 'fathers', 'fiance', 'gentleman', 'gentlemen', 'god',
            'grandfather', 'grandpa', 'grandson', 'groom', 'he', 'himself', 'husband',
            'husbands', 'king', 'male', 'man', 'mr', 'nephew', 'nephews', 'priest',
            'prince', 'son', 'sons', 'uncle', 'uncles', 'waiter', 'widower', 'widowers',

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


    # ---------------------------
    # PART 0 – GENDER DETECTION
    # ---------------------------

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

    # ---------------------------
    # PART 1 – ANALYSIS HELPERS
    # ---------------------------

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

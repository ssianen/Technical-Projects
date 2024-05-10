import sys
import re
import fileinput

class concord:
    """ concord: Represents an alphabetical list of words read from the given input and written to the given output.""" 

    def __init__(self, input=None, output=None):
      """
	    Initializes attributes of a concord instance.
	    """

        self.input = input
        self.output = output

        if self.input != None:
            self.full_concordance()

    

    def __capture_exclusion_words(self):
        """
        Reads exclusion words from input and appends them to exclusion_words[], which is then returned. 
        Also checks the version number of the test file to see if it is correct.
        """

        exclusion_words = []

        for line in fileinput.input(self.input):
            if line == '\"\"\"\"\n':
                break
            elif line != "\'\'\'\'\n":
                exclusion_words.append(line.strip().lower())
            elif line == "2\n":
                continue

        fileinput.close()
        
        version_number = exclusion_words.pop(0)  
        if version_number == '1':
            print("Input version is 1, concord4 expected version 2\n")

        return exclusion_words
    
    def __capture_index_words(self, exclusion_words):
        """
        Reads original index words from input, and appends them to original_iw[] if they are not found in exclusion_words[]. 
        Also creates a list of the uppercase version of each index word, in a similar manner to that of the original index words.
        Reads each line from input and appends the newline-stripped line to a list lines_in_file[]
        Returns sorted uppercase_iw[], unsorted original_iw[], and lines_in_file[].
        """

        lines_in_file = []
        original_iw = []
        uppercase_iw = []

        for line in fileinput.input(self.input):
            if line == "2\n":
                continue

            words_in_line = line.split()
            
            original_iw_in_line = [word.strip() for word in words_in_line if word.lower().strip() not in exclusion_words]
            original_iw.extend(original_iw_in_line)

            uppercase_iw_in_line = [word.strip().upper() for word in words_in_line if word.lower().strip() not in exclusion_words]
            uppercase_iw.extend(uppercase_iw_in_line)

            lines_in_file.append(line.strip())

        fileinput.close()
        
        uppercase_iw.sort()
        
        return uppercase_iw, original_iw, lines_in_file

    
    def __find_original_iw(self, word_to_find, original_iw):
        """
        Finds and returns the original index word as it appears in the input file, given the index word to find and original_iw[].
        """

        for original in original_iw:
            if original.lower() == word_to_find.lower():
                return original



    def __configure_spaces(self, index_word, line_to_index):
        """""
        Formats the line_to_index by slicing it in two parts: the prefix string (what comes before the index word) and the suffix string (what comes after the index word). 
        Builds the before_index string by concatenating 1 word from the prefix string at a time to ensure the total length stays within bounds. 
        Then it builds the after_index string in a similar matter.
        Returns the updated string.
        """""

        result_string = ''
        before_index = ''
        after_index = ''

        before_index_boundary = 19
        after_index_boundary = 31

        start_of_index_word = line_to_index.find(index_word)
        end_of_index_word = start_of_index_word + len(index_word)

        prefix = line_to_index[0:start_of_index_word]
        suffix = line_to_index[end_of_index_word:len(line_to_index)]

        words_of_prefix = prefix.split()
        words_of_suffix = suffix.split()

        for prefix_word in reversed(words_of_prefix):
            if len(before_index) + len(prefix_word) <= before_index_boundary:
                before_index = prefix_word + " " + before_index
            else:
                break

        for suffix_word in words_of_suffix:
            if len(after_index) + len(suffix_word) < after_index_boundary - len(index_word):
                after_index = after_index + " " + suffix_word
            else:
                break

        result_string = "{: >29}{: ^}{:>}".format(before_index, index_word, after_index)
        return result_string
       


    def __configure_lines(self, uppercase_iw, original_iw, lines_in_file):
        """""
        Finds the corresponding line in the file for each uppercase index word in sorted uppercase_i[]]. 
        Once found, the uppercase version is substituted for the index word in the line_to_index. 
        Then, the line_to_index is formatted by and appended to the result_string list if it has not already been added.
        Returns the updated list result_to_print[].
        """""

        result_to_print = []

        for index in uppercase_iw:
            for line_to_index in lines_in_file:
                    
                original = self.__find_original_iw(index, original_iw)
                if (re.search(rf'\b{original}\b', line_to_index)):

                    if original != index:
                        line_to_index = re.sub(rf'\b{original}\b', index, line_to_index)

                    result_string = self.__configure_spaces(index, line_to_index)

                    if (result_string not in result_to_print):
                        result_to_print.append(result_string)
        
        return result_to_print

    

    def full_concordance(self):
        """""
        Calls private helper instance methods to read the exclusion words, index words, and lines to index from a file.
        Creates an ordered result list of the lines based on the alphabetical order of their index words. 
        If a file name is specified, it writes this result list to a file.
        Otherwise, it returns the list result_to_print[].
        """""

        exclusion_words = self.__capture_exclusion_words()
       
        uppercase_iw, original_iw, lines_in_file = self.__capture_index_words(exclusion_words)
     
        result_to_print = self.__configure_lines(uppercase_iw, original_iw, lines_in_file)

        if self.output != None:
            file_handle = open(self.output, "w")
            file_handle.write("\n".join(result_to_print))
            file_handle.write("\n")
            file_handle.close()
        else:
            return result_to_print

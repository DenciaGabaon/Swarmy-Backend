'''TO DO:
- highest fitness score so far: 455
- the higher the fitness score, the better

- VALIDATE SCHEDULES, ROOMS, AND TIMESLOTS: MAY NAG DDOUBLE PA TAS YUNG IBANG SUBJECTS
    DI NALALAGYAN NG SCHEDULE
    sa main function if false yung validate function
     maintain the current sched and skip the update
        else, update the sched and calculate the fitness
- UNCOMMENT THE VALIDATION FUNCTION TO SEE THE ERROR
- LAB AND LEC CONSTRAINTS - done
- Dapat di lalagpas ung end time ng klase sa hour 13- done
- double booking of professor - done
- expected duration not followed - done

- MAX HOURS OF PROFESSORS PER WEEK - not yet done
-prof should have designated program

CS:
    Year 1: 10 subjects
    Year 2: 12 subjects
    Year 3: 9 subjects
    Year 4: 2 subjects
    total:  33 subjects
    total based on sections_CS: 55

IT:
    Year 1: 10 subjects
    Year 2: 12 subjects
    Year 3: 7 subjects
    Year 4: 2 subjects
    total: 31 subjects
    total based on sections_IT: 53


IS:
    Year 1: 10 subjects
    Year 2: 9 subjects
    Year 3: 7 subjects
    Year 4: 2 subjects
    total: 28 subjects
    total based on sections_IS: 47

Overall total: 155


I FOUND A POSSIBLE EASIER SOLUTION
AFTER THE VARIABLE SWARM IS DONE
WE CAN TRY to run for swarm2 where the it program is
since nakaset naman na ung for rooms and prof sa swarm1 edi macacarry over siya dapat sa swarm2
so pag nagrun ung swarm2 dapat macacarry over niya ung mga un para pag nagschedule siya alam nia ung mga naset na sa swarm1

'''

import random
from collections import defaultdict
import json


sections_cs = {
    1: ['Section 1A-CS', 'Section 1B-CS'],
    2: ['Section 2A-CS', 'Section 2B-CS'],
    3: ['Section 3A-CS'],
    4: ['Section 4A-CS']
}

sections_it = {
    1: ['Section 1A-IT', 'Section 1B-IT'],
    2: ['Section 2A-IT', 'Section 2B-IT'],
    3: ['Section 3A-IT'],
    4: ['Section 4A-IT']
}

sections_is = {
    1: ['Section 1A-IS', 'Section 1B-IS'],
    2: ['Section 2A-IS', 'Section 2B-IS'],
    3: ['Section 3A-IS'],
    4: ['Section 4A-IS']
}




professors = {
    'Prof A': {'preferred_time': 'AM', 'preferred_subjects': ['CC113-M', 'CC131L-M']},
    'Prof B': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof C': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof D': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof E': {'preferred_time': '', 'preferred_subjects': ['CS233-M', 'CS333-M']},
    'Prof F': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof G': {'preferred_time': '', 'preferred_subjects': ['CS433-M', '']},
    'Prof H': {'preferred_time': '', 'preferred_subjects': ['CS413-M', 'CS272-M']},
    'Prof I': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof J': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof K': {'preferred_time': '', 'preferred_subjects': ['', '']},
    'Prof L': {'preferred_time': '', 'preferred_subjects': ['', '']},
    # Add more professors as needed
}





#COMPUTER SCIENCE SUBJECTS

#Second Semester
subjects_CS_2 = {
    1: {'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'CC103-M': {'type': 'lec', 'units': 3}, 'CS123-M': {'type': 'lec', 'units': 3}, 'GEC2-M': {'type': 'lec', 'units': 3}, 'GEC3-M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'MATHA35-M': {'type': 'lec', 'units': 5}, 'NSTP2-M': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}},
    2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'CS201L-M': {'type': 'lab', 'units': 1}, 'CS202--M': {'type': 'lec', 'units': 2}, 'CS221L--M': {'type': 'lab', 'units': 1}, 'CS222--M': {'type': 'lec', 'units': 2}, 'CS243-M': {'type': 'lec', 'units': 3}, 'CS261L-M': {'type': 'lab', 'units': 1}, 'CS262-M': {'type': 'lec', 'units': 2}, 'PE3-M': {'type': 'lec', 'units': 3 }},
    3: {'CC303-M': {'type': 'lec', 'units': 3}, 'CS303-M': {'type': 'lec', 'units': 3}, 'CS321L-M': {'type': 'lab', 'units': 1}, 'CS322-M': {'type': 'lec', 'units': 2}, 'CS343-M': {'type': 'lec', 'units': 3}, 'CS361L-M': {'type': 'lab', 'units': 1}, 'CS362-M': {'type': 'lec', 'units': 2}, 'CSE3-M': {'type': 'lec', 'units': 3}, 'CSE4-M': {'type': 'lec', 'units': 3}},
    4: {'CS403': {'type': 'lab', 'units': 6}, 'CS423': {'type': 'lec', 'units': 3}}
}






# #COMPUTER SCIENCE NON STEM SUBJECTS
#
# # Second Semester
# subjects_CSN_2 = {
#     1: {'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'CC103-M': {'type': 'lec', 'units': 3}, 'CS123--M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'PHYSGENL-M': {'type': 'lab', 'units': 1}, 'PHYSGEN-M': {'type': 'lec', 'units': 4}, 'MATHA35-M': {'type': 'lec', 'units': 5}, 'NSTP2': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}},
#     2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'CS201L-M': {'type': 'lab', 'units': 1}, 'CS202--M': {'type': 'lec', 'units': 2}, 'CS221L--M': {'type': 'lab', 'units': 1}, 'CS222--M': {'type': 'lec', 'units': 2}, 'CS243-M': {'type': 'lec', 'units': 3}, 'CS261L-M': {'type': 'lab', 'units': 1}, 'CS262-M': {'type': 'lec', 'units': 2}},
#     3: {'CC303-M': {'type': 'lec', 'units': 3}, 'CS303-M': {'type': 'lec', 'units': 3}, 'CS321L-M': {'type': 'lab', 'units': 1}, 'CS322-M': {'type': 'lec', 'units': 2}, 'CS343-M': {'type': 'lec', 'units': 3}, 'CS361L-M': {'type': 'lab', 'units': 1}, 'CS362-M': {'type': 'lec', 'units': 2}, 'CSE3-M': {'type': 'lec', 'units': 3}, 'CSE4-M': {'type': 'lec', 'units': 3}},
#     4: {'CS403': {'type': 'lab', 'units': 6}, 'CS423': {'type': 'lec', 'units': 3}}
# }






#INFORMATION TECHNOLOGY SUBJECTS

#Second Semester
subjects_IT_2 = {
    1: {'CC103-M': {'type': 'lec', 'units': 3}, 'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'GEC2-M': {'type': 'lec', 'units': 3}, 'GEC3-M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'IT123-M': {'type': 'lec', 'units': 3}, 'MATHSTAT03-M': {'type': 'lec', 'units': 3}, 'NSTP2--M': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}},
    2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'IT201L--M': {'type': 'lec', 'units': 1}, 'IT202--M': {'type': 'lec', 'units': 2}, 'IT223-M': {'type': 'lec', 'units': 3}, 'IT241L-M': {'type': 'lab', 'units': 1}, 'IT242-M': {'type': 'lec', 'units': 2}, 'IT261L-M': {'type': 'lec', 'units': 1}, 'IT262-M': {'type': 'lec', 'units': 2}, 'ITE1-M': {'type': 'lec', 'units': 3}, 'PE4-M': {'type': 'lec', 'units': 2}},
    3: {'CC303-M': {'type': 'lec', 'units': 3}, 'GEE11D-M': {'type': 'lec', 'units': 3}, 'IT303--M': {'type': 'lec', 'units': 3}, 'IT323': {'type': 'lec', 'units': 3}, 'IT343_M': {'type': 'lec', 'units': 3}, 'IT363-M': {'type': 'lec', 'units': 3}, 'ITE4-M': {'type': 'lec', 'units': 3}},
    4: {'IT406-M': {'type': 'lab', 'units': 9}, 'IT423--M': {'type': 'lec', 'units': 3}}
}





#INFORMATION TECHNOLOGY NON STEM SUBJECTS

# #Second Semester
# subjects_ITN_2 = {
#     1: {'CC103-M': {'type': 'lec', 'units': 3}, 'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'GEC1-M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'IT123-M': {'type': 'lec', 'units': 3}, 'MATHSTAT03-M': {'type': 'lec', 'units': 3}, 'NSTP2--M': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}, 'PHYSGEN-M': {'type': 'lec', 'units': 4}, 'PHYSGENL-M': {'type': 'lab', 'units': 1}},
#     2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'IT201L--M': {'type': 'lec', 'units': 1}, 'IT202--M': {'type': 'lec', 'units': 2}, 'IT223-M': {'type': 'lec', 'units': 3}, 'IT241L--M': {'type': 'lab', 'units': 1}, 'IT242--M': {'type': 'lec', 'units': 2}, 'IT261L-M': {'type': 'lec', 'units': 1}, 'IT262-M': {'type': 'lec', 'units': 2}, 'ITE1-M': {'type': 'lec', 'units': 3}, 'PE4-M': {'type': 'lec', 'units': 2}},
#     3: {'CC303-M': {'type': 'lec', 'units': 3}, 'GEE11D-M': {'type': 'lec', 'units': 3}, 'IT303--M': {'type': 'lec', 'units': 3}, 'IT323': {'type': 'lec', 'units': 3}, 'IT343_M': {'type': 'lec', 'units': 3}, 'IT363-M': {'type': 'lec', 'units': 3}, 'ITE4-M': {'type': 'lec', 'units': 3}},
#     4: {'IT406-M': {'type': 'lab', 'units': 9}, 'IT423--M': {'type': 'lec', 'units': 3}}
# }





#INFORMATION SYSTEMS SUBJECTS

#Second Semester
subjects_IS_2 = {
    1: {'CC103-M': {'type': 'lec', 'units': 3}, 'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'GEC2-M': {'type': 'lec', 'units': 3}, 'GEC3-M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'IS123-M': {'type': 'lec', 'units': 3}, 'MATHSTAT03-M': {'type': 'lec', 'units': 3}, 'NSTP2--M': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}},
    2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'IS203-M': {'type': 'lec', 'units': 3}, 'IS223-M': {'type': 'lec', 'units': 3}, 'IS243-M': {'type': 'lec', 'units': 3}, 'IS263-M': {'type': 'lec', 'units': 3}, 'ISE1-M': {'type': 'lec', 'units': 3}, 'PE4-M': {'type': 'lec', 'units': 2}},
    3: {'CC303-M': {'type': 'lec', 'units': 3}, 'IS303-M': {'type': 'lec', 'units': 3}, 'IS323-M': {'type': 'lec', 'units': 3}, 'IS343-M': {'type': 'lec', 'units': 3}, 'IS363-M': {'type': 'lec', 'units': 3}, 'IS383-M': {'type': 'lec', 'units': 3}, 'ISE4-M': {'type': 'lec', 'units': 3}},
    4: {'IS406-M': {'type': 'lab', 'units': 9}, 'IS423-M': {'type': 'lec', 'units': 3}}
}







# #INFORMATION SYSTEMS NON STEM SUBJECTS
#
# #Second Semester
# subjects_ISN_2 = {
#     1: {'CC103-M': {'type': 'lec', 'units': 3}, 'CC141L-M': {'type': 'lab', 'units': 1}, 'CC142-M': {'type': 'lec', 'units': 2}, 'GEC1-M': {'type': 'lec', 'units': 3}, 'GEC5-M': {'type': 'lec', 'units': 3}, 'IS123-M': {'type': 'lec', 'units': 3}, 'MATHSTAT03-M': {'type': 'lec', 'units': 3}, 'NSTP2-M': {'type': 'lec', 'units': 3}, 'PE2-M': {'type': 'lec', 'units': 2}, 'PHYSGEN-M': {'type': 'lec', 'units': 4}, 'PHYSGENL-M': {'type': 'lab', 'units': 1}},
#     2: {'CC201L-M': {'type': 'lab', 'units': 1}, 'CC202-M': {'type': 'lec', 'units': 2}, 'CC223-M': {'type': 'lec', 'units': 3}, 'IS203-M': {'type': 'lec', 'units': 3}, 'IS223-M': {'type': 'lec', 'units': 3}, 'IS243-M': {'type': 'lec', 'units': 3}, 'IS263-M': {'type': 'lec', 'units': 3}, 'ISE1-M': {'type': 'lec', 'units': 3}, 'PE4-M': {'type': 'lec', 'units': 2}},
#     3: {'CC303-M': {'type': 'lec', 'units': 3}, 'IS303-M': {'type': 'lec', 'units': 3}, 'IS323-M': {'type': 'lec', 'units': 3}, 'IS343-M': {'type': 'lec', 'units': 3}, 'IS363-M': {'type': 'lec', 'units': 3}, 'IS383-M': {'type': 'lec', 'units': 3}, 'ISE4-M': {'type': 'lec', 'units': 3}},
#     4: {'IS406-M': {'type': 'lab', 'units': 9}, 'IS423-M': {'type': 'lec', 'units': 3}}
# }



sections = {
    'CS': sections_cs,
    'IT': sections_it,
    'IS': sections_is

}
subjects = {
    'CS': subjects_CS_2,
    'IT': subjects_IT_2,
    'IS': subjects_IS_2
}



rooms = ['Room 320', 'Room 321', 'Room 322', 'Room 324', 'Room 326','Room 328', 'Room DOST-A', 'Room DOST-B', 'Room BODEGA-A', 'Room BODEGA-b']


time_slots = {
    'D1_H1': {'day': 'Monday', 'start': 7, 'end': 8},
    'D1_H2': {'day': 'Monday', 'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'D1_H3': {'day': 'Monday', 'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'D1_H4': {'day': 'Monday', 'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'D1_H5': {'day': 'Monday', 'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'D1_H6': {'day': 'Monday', 'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'D1_H7': {'day': 'Monday', 'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'D1_H8': {'day': 'Monday', 'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'D1_H9': {'day': 'Monday', 'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'D1_H10': {'day': 'Monday', 'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'D1_H11': {'day': 'Monday', 'start': 17, 'end': 18},  # 5:00 PM to 6:00 PM
    'D1_H12': {'day': 'Monday', 'start': 18, 'end': 19},
    'D1_H13': {'day': 'Monday', 'start': 19, 'end': 20},


    'D2_H1': {'day': 'Tuesday', 'start': 7, 'end': 8},
    'D2_H2': {'day': 'Tuesday', 'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'D2_H3': {'day': 'Tuesday', 'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'D2_4': {'day': 'Tuesday', 'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'D2_H5': {'day': 'Tuesday', 'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'D2_H6': {'day': 'Tuesday', 'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'D2_H7': {'day': 'Tuesday', 'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'D2_H8': {'day': 'Tuesday', 'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'D2_H9': {'day': 'Tuesday', 'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'D2_H10': {'day': 'Tuesday', 'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'D2_H11': {'day': 'Tuesday', 'start': 17, 'end': 18},  # 5:00 PM to 6:00 PM
    'D2_H12': {'day': 'Tuesday', 'start': 18, 'end': 19},
    'D2_H13': {'day': 'Tuesday', 'start': 19, 'end': 20},


    'D3_H1': {'day': 'Wednesday', 'start': 7, 'end': 8},
    'D3_H2': {'day': 'Wednesday', 'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'D3_H3': {'day': 'Wednesday', 'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'D3_4': {'day': 'Wednesday', 'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'D3_H5': {'day': 'Wednesday', 'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'D3_H6': {'day': 'Wednesday', 'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'D3_H7': {'day': 'Wednesday', 'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'D3_H8': {'day': 'Wednesday', 'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'D3_H9': {'day': 'Wednesday', 'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'D3_H10': {'day': 'Wednesday', 'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'D3_H11': {'day': 'Wednesday', 'start': 17, 'end': 18},  # 5:00 PM to 6:00 PM
    'D3_H12': {'day': 'Wednesday', 'start': 18, 'end': 19},
    'D3_H13': {'day': 'Wednesday', 'start': 19, 'end': 20},


    'D4_H1': {'day': 'Thursday', 'start': 7, 'end': 8},
    'D4_H2': {'day': 'Thursday', 'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'D4_H3': {'day': 'Thursday', 'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'D4_4': {'day': 'Thursday', 'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'D4_H5': {'day': 'Thursday', 'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'D4_H6': {'day': 'Thursday', 'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'D4_H7': {'day': 'Thursday', 'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'D4_H8': {'day': 'Thursday', 'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'D4_H9': {'day': 'Thursday', 'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'D4_H10': {'day': 'Thursday', 'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'D4_H11': {'day': 'Thursday', 'start': 17, 'end': 18},  # 5:00 PM to 6:00 PM
    'D4_H12': {'day': 'Thursday', 'start': 18, 'end': 19},
    'D4_H13': {'day': 'Thursday', 'start': 19, 'end': 20},


    'D5_H1': {'day': 'Friday', 'start': 7, 'end': 8},
    'D5_H2': {'day': 'Friday', 'start': 8, 'end': 9},  # 8:00 AM to 9:00 AM
    'D5_H3': {'day': 'Friday', 'start': 9, 'end': 10},  # 9:00 AM to 10:00 AM
    'D5_H4': {'day': 'Friday', 'start': 10, 'end': 11},  # 10:00 AM to 11:00 AM
    'D5_H5': {'day': 'Friday', 'start': 11, 'end': 12},  # 11:00 AM to 12:00 PM
    'D5_H6': {'day': 'Friday', 'start': 12, 'end': 13},  # 12:00 PM to 1:00 PM
    'D5_H7': {'day': 'Friday', 'start': 13, 'end': 14},  # 1:00 PM to 2:00 PM
    'D5_H8': {'day': 'Friday', 'start': 14, 'end': 15},  # 2:00 PM to 3:00 PM
    'D5_H9': {'day': 'Friday', 'start': 15, 'end': 16},  # 3:00 PM to 4:00 PM
    'D5_H10': {'day': 'Friday', 'start': 16, 'end': 17},  # 4:00 PM to 5:00 PM
    'D5_H11': {'day': 'Friday', 'start': 17, 'end': 18},  # 5:00 PM to 6:00 PM
    'D5_H12': {'day': 'Friday', 'start': 18, 'end': 19},
    'D5_H13': {'day': 'Friday', 'start': 19, 'end': 20}

}





swarm_size = 60
max_iterations = 100
w = 0.5
c1 = 1.5
c2 = 1.5
max_classes_per_day = 6  # Set this to the maximum number of classes you want per day
max_teaching_hours = 30  # Maximum teaching hours allowed per professor


class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fitness = float('-inf')
        self.pBest = position
        self.pBest_fitness = float('-inf')


# def initialize_particle(sec_cs, sec_it, sec_is, subject_cs, subject_it, subject_is,  professors, time_slots, rooms, max_attempts=1000):
#     # Group time slots by day and time period (AM/PM)
#     time_slots_by_day = defaultdict(lambda: {'AM': [], 'PM': []})
#     for ts_id, ts_info in time_slots.items():
#         period = 'AM' if 7 <= ts_info['start'] < 12 else 'PM'
#         time_slots_by_day[ts_info['day']][period].append((ts_id, ts_info))
#
#         # Sort time slots within each day and period by start time
#         for day in time_slots_by_day:
#             time_slots_by_day[day]['AM'].sort(key=lambda ts: ts[1]['start'])
#             time_slots_by_day[day]['PM'].sort(key=lambda ts: ts[1]['start'])
#
#     for _ in range(max_attempts):
#         schedule = []
#         assigned_subjects = set()
#         section_time_slots = defaultdict(list)  # Store the used time slots for each section
#         section_day_classes = defaultdict(lambda: defaultdict(int))  # Store the number of classes for each day for each section
#         section_assigned_subjects = defaultdict(set)  # Store the assigned subjects for each section
#         professor_time_slots = defaultdict(set)  # Store the used time slots for each professor
#         professor_hours_taught = defaultdict(int) # Store the total teaching hours for each professor
#         print(subjects)
#         for year, year_sections in sections.items():
#             for section in year_sections:
#                 subject_pool = subjects[year].copy()  # Create a copy of the subjects for this year
#                 while subject_pool:  # While there are still subjects to be scheduled
#                     subject = random.choice(list(subject_pool.keys()))
#                     del subject_pool[subject]  # Remove the subject from the pool
#
#                     # Skip this subject if it has already been assigned to this section
#                     if subject in section_assigned_subjects[section]:
#                         continue
#
#                     available_professors = [prof for prof in professors if subject in professors[prof]['preferred_subjects']]
#                     if not available_professors:
#                         #print(f"No preferred professor for {subject}. Using any professor.")
#                         available_professors = list(professors.keys())  # Fallback to any professor if still empty
#
#                     subject_units = subjects[year][subject]['units']
#                     subject_type = subjects[year][subject]['type']
#                     expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units
#
#                      # Check if any professor has not exceeded the teaching hours limit
#                     professors_within_limit = [prof for prof in available_professors if professor_hours_taught[prof] + expected_duration <= max_teaching_hours]
#
#                     if not professors_within_limit:
#                         #print(f"No professor available within the teaching hours limit for {subject} in {section}. Skipping.")
#                         professor = random.choice(available_professors)  # Fallback to any professor if still empty
#                     else:
#                         #print(f"Available professors within the teaching hours limit for {subject} in {section}: {professors_within_limit}")
#                         professor = random.choice(professors_within_limit)
#
#                     #print(f"Expected Duration for {subject} in {section}: {expected_duration}")
#
#                     # Determine preferred period (AM/PM) for the professor
#                     if professors[professor]['preferred_time']:
#                         preferred_period = 'AM' if 'AM' in professors[professor]['preferred_time'] else 'PM'
#                         #print(f"Preferred time of {professor} for {subject}: {professors[professor]['preferred_time']}")
#                     else:
#                         #print(f"No preferred time for {professor}. Using any period.")
#                         preferred_period = None
#
#                     # Find all ranges of consecutive time slots that can accommodate the expected duration
#                     suitable_time_slot_ranges = []
#                     preferred_time_slot_ranges = []
#
#                     # Check consecutive time slots within each day
#                     for day, periods in time_slots_by_day.items():
#                         for period, slots in periods.items():
#                             for i in range(len(slots) - expected_duration + 1):
#                                 time_slot_range = slots[i:i + expected_duration]
#                                 time_slot_ids = [ts[0] for ts in time_slot_range]
#
#                                 # Check if all time slots in the range are available for the section and professor
#                                 if all(ts not in section_time_slots[section] and ts not in professor_time_slots[professor] for ts in time_slot_ids):
#                                     if all(section_day_classes[section][day] < max_classes_per_day for ts in time_slot_ids):
#                                         suitable_time_slot_ranges.append(time_slot_ids)
#                                         # Prioritize the preferred time slot ranges
#                                         if period == preferred_period:
#                                             #print(f"Preferred Time Slot Range found for {subject} in {section} on {day} {period}. Using it.")
#                                             preferred_time_slot_ranges.append(time_slot_ids)
#
#                     # Prioritize preferred time slot ranges if available
#                     if preferred_time_slot_ranges:
#                         selected_time_slot_ranges = preferred_time_slot_ranges
#                         #print(f"Preferred Time Slot Range found for {subject} in {section}. Using it.")
#                     else:
#                         #print(f"No preferred time slot range found for {subject} in {section}. Using any suitable range.")
#                         selected_time_slot_ranges = suitable_time_slot_ranges
#
#                     if not selected_time_slot_ranges:  # If no suitable range of time slots is found, skip this subject
#                         #print(f"No suitable time slot range found for {subject} in {section}. Skipping.")
#                         continue
#
#                     # Randomly select a suitable range of time slots
#                     time_slot_ids = random.choice(suitable_time_slot_ranges)
#                     #print(f"Selected Time Slots for {subject} in {section}: {time_slot_ids}")
#
#                     # Add the used time slots to the section's list and increment the number of classes for each day
#                     section_time_slots[section].extend(time_slot_ids)
#                     professor_time_slots[professor].update(time_slot_ids)
#                     for ts in time_slot_ids:
#                         section_day_classes[section][time_slots[ts]['day']] += 1
#
#                     room = random.choice(rooms)
#
#                     # Add an entry to the schedule for each time slot in the range
#                     for time_slot in time_slot_ids:
#                         schedule.append((section, subject, professor, time_slot, room))
#                         #print(f"Added {subject} in {section} at {time_slot} with {professor} in {room}")
#
#                     # Add the subject to the section's assigned subjects
#                     section_assigned_subjects[section].add(subject)
#
#                     # Update the total teaching hours for the professor
#                     professor_hours_taught[professor] += expected_duration
#
#                     # Check if the professor has exceeded the maximum teaching hours
#                     #if professor_hours_taught[professor] > max_teaching_hours:
#                         #print(f"Professor {professor} has exceeded the maximum teaching hours. {professor_hours_taught[professor]}")
#
#
#         # Validate the generated schedule
#         validated_schedule = validate_position(schedule)
#         if validated_schedule:
#             #print("Valid Schedule Found!", validated_schedule)
#             return schedule
#
#     # If no valid schedule is found after maximum attempts, return None
#     return None




def initialize_particle(sections, subjects, professors, time_slots, rooms, max_attempts=1000, max_teaching_hours=30, max_classes_per_day=6):
    # Categorize time slots by day and period
    time_slots_by_day = defaultdict(lambda: {'AM': [], 'PM': []})
    for ts_id, ts_info in time_slots.items():
        period = 'AM' if 7 <= ts_info['start'] < 12 else 'PM'
        time_slots_by_day[ts_info['day']][period].append((ts_id, ts_info))

    # Sort time slots by start time within each period
    for day in time_slots_by_day:
        time_slots_by_day[day]['AM'].sort(key=lambda ts: ts[1]['start'])
        time_slots_by_day[day]['PM'].sort(key=lambda ts: ts[1]['start'])

    for _ in range(max_attempts):
        schedule = []
        section_time_slots = defaultdict(list)
        section_day_classes = defaultdict(lambda: defaultdict(int))
        section_assigned_subjects = defaultdict(set)
        professor_time_slots = defaultdict(set)
        professor_hours_taught = defaultdict(int)

        for program, year_sections in sections.items():
            for year, section_list in year_sections.items():
                for section in section_list:
                    subject_pool = list(subjects[program][year].keys())
                    while subject_pool:
                        subject = random.choice(subject_pool)
                        subject_pool.remove(subject)

                        if subject in section_assigned_subjects[section]:
                            continue

                        available_professors = [prof for prof in professors if subject in professors[prof]['preferred_subjects']]
                        if not available_professors:
                            available_professors = list(professors.keys())

                        subject_info = subjects[program][year][subject]
                        if 'units' not in subject_info or 'type' not in subject_info:
                            continue

                        subject_units = subject_info['units']
                        subject_type = subject_info['type']
                        expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

                        professors_within_limit = [prof for prof in available_professors if professor_hours_taught[prof] + expected_duration <= max_teaching_hours]

                        if not professors_within_limit:
                            professor = random.choice(available_professors)
                        else:
                            professor = random.choice(professors_within_limit)

                        preferred_period = 'AM' if 'AM' in professors[professor]['preferred_time'] else 'PM'

                        suitable_time_slot_ranges = []
                        preferred_time_slot_ranges = []

                        for day, periods in time_slots_by_day.items():
                            for period, slots in periods.items():
                                for i in range(len(slots) - expected_duration + 1):
                                    time_slot_range = slots[i:i + expected_duration]
                                    time_slot_ids = [ts[0] for ts in time_slot_range]

                                    if all(ts not in section_time_slots[section] and ts not in professor_time_slots[professor] for ts in time_slot_ids):
                                        if all(section_day_classes[section][day] < max_classes_per_day for ts in time_slot_ids):
                                            suitable_time_slot_ranges.append(time_slot_ids)
                                            if period == preferred_period:
                                                preferred_time_slot_ranges.append(time_slot_ids)

                        if preferred_time_slot_ranges:
                            selected_time_slot_ranges = preferred_time_slot_ranges
                        else:
                            selected_time_slot_ranges = suitable_time_slot_ranges

                        if not selected_time_slot_ranges:
                            continue

                        time_slot_ids = random.choice(selected_time_slot_ranges)

                        section_time_slots[section].extend(time_slot_ids)
                        professor_time_slots[professor].update(time_slot_ids)
                        for ts in time_slot_ids:
                            section_day_classes[section][time_slots[ts]['day']] += 1

                        room = random.choice(rooms)

                        for time_slot in time_slot_ids:
                            schedule.append((section, subject, professor, time_slot, room))

                        section_assigned_subjects[section].add(subject)
                        professor_hours_taught[professor] += expected_duration


        print("Schedule: ", schedule)
        validated_schedule = validate_position(schedule)
        if validated_schedule:
            return schedule

    return None


def initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms):
    swarm = []
    for _ in range(swarm_size):
        position = None
        while position is None:
            position = initialize_particle(sections, subjects, professors, time_slots, rooms)
            #print("Initial Position: ", position)
            position, _ = adjust_schedule(position)
        velocity = [0] * len(position)  # Initial velocity
        swarm.append(Particle(position, velocity))
    return swarm



def preference_score(professor, time_slot):
    preferred_time = professors[professor]['preferred_time']
    if preferred_time in time_slot:
        return 10
    return 5


def get_subject_year(subject):
    # Placeholder for the actual logic to determine the year of the subject
    for program in subjects:
        for year in subjects[program]:
            if subject in subjects[program][year]:
                return year
    return None


# def get_subject_year(subject):
#     print("Subject: ", subject)
#     for year, subjects_in_year in subjects_CS_1.items():
#         if subject in subjects_in_year:
#             return year
#     return None




def calculate_conflicts(schedule):
    print("schedule_calc: ", schedule)

    conflicts = 0
    time_room_usage = {}
    time_professor_usage = {}

    for (section, subject, professor, time_slot, room) in schedule:
        year = get_subject_year(subject)
        if year is None:
            print(f"Error: Year not found for subject {subject}")
            continue

        if "CS" in section:
            program = "CS"
        elif "IT" in section:
            program = "IT"
        elif "IS" in section:
            program = "IS"
        else:
            program = "Unknown"

        time_slot_start = time_slots[time_slot]['start']
        if subjects[program][year][subject]['type'] == 'lec':
            time_slot_end = time_slot_start + subjects[program][year][subject]['units']  # 1 hour for lecture
        else:
            time_slot_end = time_slot_start + subjects[program][year][subject]['units'] * 3  # 3 hours for lab

        # Check for room conflict
        for (used_time_slot, used_room) in time_room_usage.keys():
            used_time_slot_start = time_slots[used_time_slot]['start']
            used_time_slot_end = time_slots[used_time_slot]['end']

            if room == used_room and not (time_slot_end <= used_time_slot_start or time_slot_start >= used_time_slot_end):
                #print(f"Room conflict detected for {room} at {time_slot}.")
                conflicts += 1
        time_room_usage[(time_slot, room)] = True

        # Check for professor conflict
        for (used_time_slot, used_professor) in time_professor_usage.keys():
            used_time_slot_start = time_slots[used_time_slot]['start']
            used_time_slot_end = time_slots[used_time_slot]['end']

            if professor == used_professor and not (time_slot_end <= used_time_slot_start or time_slot_start >= used_time_slot_end):
                #print(f"Professor conflict detected for {professor} at {time_slot}.")
                conflicts += 1
        time_professor_usage[(time_slot, professor)] = True

    return conflicts

def calculate_distribution(schedule):
    teacher_gaps = 0
    for professor in professors:
        times = [time_slot for (section, subject, prof, time_slot, room) in schedule if prof == professor]
        teacher_gaps += len(set(times))
    return -teacher_gaps


def calculate_fitness(schedule):
    schedule, conflicts_resolved = adjust_schedule(schedule)
    preference_scores = sum(preference_score(prof, time_slot) for (section, subject, prof, time_slot, room) in schedule)
    conflict_penalty = calculate_conflicts(schedule)
    distribution_score = calculate_distribution(schedule)
    return preference_scores - conflict_penalty + distribution_score

position_to_num = {}
num_to_position = {}


def convert_to_numeric(position):
    global position_to_num, num_to_position
    if position not in position_to_num:
        num = len(position_to_num)
        position_to_num[position] = num
        num_to_position[num] = position
    return position_to_num[position]

def convert_from_numeric(num):
    global num_to_position
    return num_to_position[num]



def update_velocity(particle, gBest, w, c1, c2):
    new_velocity = []
    for i in range(len(particle.position)):
        if i < len(gBest):
            gBest_num = convert_to_numeric(gBest[i])
            r1 = random.random()
            r2 = random.random()

            pos_num = convert_to_numeric(particle.position[i])
            pBest_num = convert_to_numeric(particle.pBest[i])
            gBest_num = convert_to_numeric(gBest[i])

            cognitive = c1 * r1 * (pBest_num - pos_num)
            social = c2 * r2 * (gBest_num - pos_num)

            new_velocity.append(w * (particle.velocity[i] if particle.velocity else 0) + cognitive + social)
    return new_velocity

def update_position(particle):
    new_position = []
    num_positions = len(num_to_position)

    if num_positions == 0:
        raise ValueError("The num_to_position dictionary is empty. Ensure it is properly initialized.")

    for i in range(len(particle.position)):
        current_pos = particle.position[i]
        current_pos_num = convert_to_numeric(current_pos)

        new_pos_num = (round(current_pos_num + particle.velocity[i]) % num_positions)

        if new_pos_num < 0:
            new_pos_num += num_positions

        new_pos = convert_from_numeric(new_pos_num)
        new_position.append(new_pos)

    return new_position




def validate_position(position):
    professor_schedule = defaultdict(set)
    room_schedule = defaultdict(set)
    section_subjects = defaultdict(set)

    print("Position: ", position)

    i = 0
    while i < len(position):
        section, subject, professor, time_slot, room = position[i]

        print("professor: ", professor)
        print("time_slot: ", time_slot)
        print("room: ", room)
        print("section: ", section)
        print("subject: ", subject)

        # Check for double booking for professors
        if professor in professor_schedule and time_slot in professor_schedule[professor]:
            adjusted_event = adjust_event(position[i])
            if adjusted_event is None:  # If adjustment fails
                print(f"Double booking detected for professor {professor} at {time_slot}. Cannot be changed")
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event
        professor_schedule[professor].add(time_slot)

        # Check for double booking for rooms
        if room in room_schedule and time_slot in room_schedule[room]:
            adjusted_event = adjust_event(position[i])
            if adjusted_event is None:  # If adjustment fails
                print(f"Double booking detected for room {room} at {time_slot}. Cannot change")
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event
        room_schedule[room].add(time_slot)

        print("section: ", section)

        # Check for double subjects per section
        if subject in section_subjects[section]:
            del position[i]  # Remove the duplicate subject
            continue  # Skip the increment of i
        section_subjects[section].add(subject)

        print("section subs: ", section_subjects)

        # Validate the duration of each subject based on its units
        year = get_subject_year(subject)
        print("Year: ", year)

        # for program, year_sections in sections.items():
        #     for year, section_list in year_sections.items():

        # Check the conditions and set the program variable accordingly
        if "CS" in section:
            program = "CS"
        elif "IT" in section:
            program = "IT"
        elif "IS" in section:
            program = "IS"
        else:
            program = "Unknown"

        subject_info = subjects[program][year][subject]
        if 'units' not in subject_info or 'type' not in subject_info:
            continue

        subject_units = subject_info['units']
        subject_type = subject_info['type']
        expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

        # subject_units = subjects_CS_2[year][subject]['units']
        # subject_type = subjects_CS_2[year][subject]['type']
        # expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

        actual_duration = time_slots[time_slot]['end'] - time_slots[time_slot]['start']
        if actual_duration != expected_duration:
            adjusted_event = adjust_event(position[i])
            if adjusted_event is None:  # If adjustment fails
                print(f"Invalid duration for {subject_type} {subject} in section {section} at {time_slot}. Cannot be adjusted")
                return None
            position[i] = adjusted_event  # Replace the conflicting event with the adjusted event

        i += 1  # Increment i

    return position

def adjust_schedule(schedule):
    #Generalize the identification of conflicts (computer studies)
    #print("adjust_sched: ", schedule)
    conflicts_resolved = 0
    # Iterate through the schedule to identify conflicts
    for i, event1 in enumerate(schedule):
        for j, event2 in enumerate(schedule[i + 1:]):  # Avoid double-checking pairs
            j += i + 1  # Adjust index to account for slicing
            # Check for double booking
            if event1[3] == event2[3] and (event1[4] == event2[4] or event1[2] == event2[2]):
                # Resolve conflict by adjusting one of the events
                if random.choice([True, False]):  # Randomly choose which event to adjust
                    event1 = adjust_event(event1)
                else:
                    event2 = adjust_event(event2)
                schedule[i] = event1
                schedule[j] = event2
                conflicts_resolved += 1

    #print(f"Conflicts resolved: {conflicts_resolved}")
    return schedule, conflicts_resolved



def adjust_event(event):
    section, subject, professor, time_slot, room = event
    year = get_subject_year(subject)
    # subject_units = subjects_CS_2[year][subject]['units']
    # subject_type = subjects_CS_2[year][subject]['type']
    # expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

    if "CS" in section:
        program = "CS"
    elif "IT" in section:
        program = "IT"
    elif "IS" in section:
        program = "IS"
    else:
        program = "Unknown"

    subject_info = subjects[program][year][subject]
    # if 'units' not in subject_info or 'type' not in subject_info:
    #     continue

    subject_units = subject_info['units']
    subject_type = subject_info['type']
    expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

    # Adjust the event by changing its time slot or room
    event = list(event)  # Convert tuple to list for modification

    # Choose a new random time slot that can accommodate the expected duration
    available_time_slots = [ts for ts in time_slots if time_slots[ts]['end'] - time_slots[ts]['start'] >= expected_duration]
    # dito magaadjust ng time slot for starting sa hapon
    # Exclude the last two time slots of the day for lab subjects or lecture subjects with 3 units
    if subject_type == 'lab' or (subject_type == 'lec' and subject_units >= 2):
        available_time_slots = [ts for ts in available_time_slots if not ts.endswith('_H12') and not ts.endswith('_H13')]
    # Exclude the last four time slots of the day for lecture subjects with 5 units
    elif subject_type == 'lec' and subject_units == 5:
        available_time_slots = [ts for ts in available_time_slots if not ts.endswith('_H10') and not ts.endswith('_H11') and not ts.endswith('_H12') and not ts.endswith('_H13')]

    if available_time_slots:
        event[3] = random.choice(available_time_slots)

    event[4] = random.choice(rooms)  # Choose a new random room

    return tuple(event)

'''def adjust_event(event):
    section, subject, professor, time_slot, room = event
    year = get_subject_year(subject)
    subject_units = subjects[year][subject]['units']
    subject_type = subjects[year][subject]['type']
    expected_duration = subject_units * 3 if subject_type == 'lab' else subject_units

    # Adjust the event by changing its time slot or room
    event = list(event)  # Convert tuple to list for modification

    # Choose a new random time slot that can accommodate the expected duration
    available_time_slots = [ts for ts in time_slots if time_slots[ts]['end'] - time_slots[ts]['start'] >= expected_duration]
    if available_time_slots:
        event[3] = random.choice(available_time_slots)

    event[4] = random.choice(rooms)  # Choose a new random room

    return tuple(event)
'''
# Example usage:



'''def validate_position(position):
    # Validate the position (e.g., no double-booking)
    return position'''



def print_timetable(schedule):
    # Group the schedule by day and section
    grouped_schedule = defaultdict(lambda: defaultdict(list))
    for entry in schedule:
        day, section = entry[3].split('_')[0], entry[0]  # Extract the day and section from the entry
        grouped_schedule[day][section].append(entry)

    # Define the order of the days
    days_order = ['D1', 'D2', 'D3', 'D4', 'D5']

    # Print the timetable
    for day in days_order:
        print(f"\n{day}:")
        for section, entries in grouped_schedule[day].items():
            print(f"  {section}:")
            # Sort the entries by the start time of the time slot
            sorted_entries = sorted(entries, key=lambda entry: entry[3])
            for entry in sorted_entries:
                section, subject, professor, time_slot, room = entry
                print(f"    {time_slot}: {subject} with {professor} in {room}")


def group_schedule_by_section(schedule):
    grouped_schedule = defaultdict(list)
    for entry in schedule:
        section = entry[0]
        grouped_schedule[section].append(entry)
    return grouped_schedule


def swarmy(intialize_swarm):
    gBest = None
    gBest_fitness = float('-inf')
    # print("initial gBest: ", gBest)
    n = 0
    # print("Swarm Initialized:", swarm)
    # Evaluate initial fitness
    for particle in intialize_swarm:
        particle.fitness = calculate_fitness(particle.position)
        particle.pBest = particle.position
        particle.pBest_fitness = particle.fitness
        if particle.fitness > gBest_fitness:
            gBest = particle.position
            gBest_fitness = particle.fitness
            # print("particle.fitness > gBest_fitness: ", gBest)
        # Iterate
    for iteration in range(max_iterations):
        for particle in intialize_swarm:
            # print(particle, gBest, w, c1, c2)
            # print("Particle Position:", particle.position)
            # print("Particle Velocity:", particle.velocity)
            particle.velocity = update_velocity(particle, gBest, w, c1, c2)
            # print("PARTICLE.position TYPE: ", type(particle.position))
            # print("before update: ", particle.position)
            # particle_instance = Particle(list(particle.), [0] * len(particle))  # Create a Particle instance
            particle.position, _ = adjust_schedule(particle.position)
            particle.position = update_position(particle)
            # print("after update: ", particle.position)
            particle.position = validate_position(particle.position)
            # print("after validate: ", particle.position)

            if particle.position:
                particle.fitness = calculate_fitness(particle.position)
                if particle.fitness > particle.pBest_fitness:
                    particle.pBest = particle.position
                    particle.pBest_fitness = particle.fitness
                if particle.fitness > gBest_fitness:
                    # print("particle position in >gBest:", particle.position)
                    gBest = particle.position
                    gBest_fitness = particle.fitness
            else:
                print("Skipping fitness calculation due to invalid position.")

    # print("Final gBest:", gBest)
    # swarm2 = initialize_swarm(swarm_size, sections_it, subjects_IT_2, professors, time_slots, rooms)

    # The gBest now holds the best found schedule
    # This print statement is for the division per section of the overall schedule
    grouped_schedule = group_schedule_by_section(gBest)

    print("Optimized CS Schedule:")
    for section, entries in grouped_schedule.items():
        print(f"\n{section}:")
        for entry in entries:
            n += 1
            print(f"{n}. {entry}")
    print("\nFitness Score:", gBest_fitness)

    print_timetable(gBest)

    json_schedule = {section: [list(entry) for entry in entries] for section, entries in grouped_schedule.items()}

    # Save the schedule to a JSON file
    with open('schedule.json', 'w') as f:
        json.dump(json_schedule, f, indent=4)


def main():
    # Initialize swarm
    swarm = initialize_swarm(swarm_size, sections, subjects, professors, time_slots, rooms)
    #swarm_it = initialize_swarm(swarm_size, sections_it, subjects_IT_2, professors, time_slots, rooms)
    #swarm_is = initialize_swarm(swarm_size, sections_is, subjects_IS_2, professors, time_slots, rooms)

    swarmy(swarm)
    #swarm(swarm_it)


    #print("Swarm size:", swarm_size)
    #each particle in swarm is an instance or memory address of where the particle is located
    # Initialize gBest to the position of the first particle in the swarm

    #COMPUTER SCIENCE----------------------------------------------------
    # gBest = None
    # gBest_fitness = float('-inf')
    # #print("initial gBest: ", gBest)
    # n = 0
    # #print("Swarm Initialized:", swarm)
    # # Evaluate initial fitness
    # for particle in swarm_cs:
    #     particle.fitness = calculate_fitness(particle.position)
    #     particle.pBest = particle.position
    #     particle.pBest_fitness = particle.fitness
    #     if particle.fitness > gBest_fitness:
    #         gBest = particle.position
    #         gBest_fitness = particle.fitness
    #         #print("particle.fitness > gBest_fitness: ", gBest)
    #     # Iterate
    # for iteration in range(max_iterations):
    #     for particle in swarm_cs:
    #         #print(particle, gBest, w, c1, c2)
    #         #print("Particle Position:", particle.position)
    #         #print("Particle Velocity:", particle.velocity)
    #         particle.velocity = update_velocity(particle, gBest, w, c1, c2)
    #         #print("PARTICLE.position TYPE: ", type(particle.position))
    #         #print("before update: ", particle.position)
    #         #particle_instance = Particle(list(particle.), [0] * len(particle))  # Create a Particle instance
    #         particle.position, _ = adjust_schedule(particle.position)
    #         particle.position = update_position(particle)
    #         #print("after update: ", particle.position)
    #         particle.position = validate_position(particle.position)
    #         #print("after validate: ", particle.position)
    #
    #         if particle.position:
    #             particle.fitness = calculate_fitness(particle.position)
    #             if particle.fitness > particle.pBest_fitness:
    #                 particle.pBest = particle.position
    #                 particle.pBest_fitness = particle.fitness
    #             if particle.fitness > gBest_fitness:
    #                 #print("particle position in >gBest:", particle.position)
    #                 gBest = particle.position
    #                 gBest_fitness = particle.fitness
    #         else:
    #             print("Skipping fitness calculation due to invalid position.")
    #
    # #print("Final gBest:", gBest)
    # #swarm2 = initialize_swarm(swarm_size, sections_it, subjects_IT_2, professors, time_slots, rooms)
    #
    # # The gBest now holds the best found schedule
    # # This print statement is for the division per section of the overall schedule
    # grouped_schedule = group_schedule_by_section(gBest)
    #
    #
    # print("Optimized CS Schedule:")
    # for section, entries in grouped_schedule.items():
    #     print(f"\n{section}:")
    #     for entry in entries:
    #         n += 1
    #         print(f"{n}. {entry}")
    # print("\nFitness Score:", gBest_fitness)

    #Di pa nalalagay -----------------------------------------------------------
    #print_timetable(gBest)
    # exporting to json
    # Convert the schedule to a format suitable for JSON
    # json_schedule = {section: [list(entry) for entry in entries] for section, entries in grouped_schedule.items()}
    #
    # # Save the schedule to a JSON file
    # with open('schedule.json', 'w') as f:
    #     json.dump(json_schedule, f, indent=4)
    #-------------------------------------------------------------------------


    # The gBest now holds the best found schedule
    # This print statement is for you to see the overall schedule
    '''print("Optimized Schedule:\n" + '\n'.join(f"{n+i+1}. {entry}" for i, entry in enumerate(gBest)))
    print("Fitness Score:", gBest_fitness)'''

if __name__ == "__main__":
    main()




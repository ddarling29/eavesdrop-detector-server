import subprocess
import shutil
import os
import csv


def detect_eavesdrop(scan, filename, extension):
    subprocess.call(['./openface/build/bin/FaceLandmarkImg', '-f', 'data/' + filename + extension])
    result = False
    if scan:
        if os.path.isfile('processed/' + filename + '.csv'):
            with open('processed/' + filename + '.csv') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    gaze_x = float(row[8])
                    gaze_y = float(row[9])

                    if 0.1 > gaze_x > -0.1 and 0.1 > gaze_y > -0.1:
                        print(gaze_x)
                        print(gaze_y)
                        result = True
    else:
        if os.path.isfile('processed/' + filename + '.csv'):
            with open('processed/' + filename + '.csv') as csv_file:
                reader = csv.reader(csv_file)
                gaze_angles = []
                largest_head = 0
                curr_max_size = 0
                head_num = 0
                next(reader)
                for row in reader:
                    if (float(row[312]) - float(row[296])) * (float(row[372]) - float(row[388])) > curr_max_size:
                        curr_max_size = (float(row[312]) - float(row[296])) * (float(row[372]) - float(row[388]))
                        largest_head = head_num
                    gaze_angles.append((row[8], row[9]))
                    head_num += 1

                head_num = 0
                for angles in gaze_angles:
                    if head_num == largest_head:
                        head_num += 1
                        continue
                    else:
                        gaze_x = float(angles[0])
                        gaze_y = float(angles[1])
                        if 0.1 > gaze_x > -0.1 and 0.1 > gaze_y > -0.1:
                            print(head_num)
                            result = True
                    head_num += 1

    shutil.rmtree('processed/')
    return result

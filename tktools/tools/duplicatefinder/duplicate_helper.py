# -*- coding:utf-8 -*-
'''
 * @Author: tyhye.wang 
 * @Date: 2018-07-09 21:30:45 
 * @Last Modified by:   tyhye.wang 
 * @Last Modified time: 2018-07-09 21:30:45 
'''

import cv2
import datetime
import numpy as np
import tkinter as tk
import os


import threading
import time

# class ComputeThread (threading.Thread):
#     def __init__(self, threadID, name, image_list, image_dir='./', threshold=0.8,btnvar=None, btn=None, listbox=None, logvar=None, log_label=None):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.__running = threading.Event()
#         self.__running.set()

#         self.computer = Similarity_Computer()
#         self.image_list = image_list
#         self.image_dir = image_dir
#         self.threshold=threshold
#         self.btn = btn
#         self.listbox = listbox
#         self.logvar = logvar
#         self.log_label = log_label
    
#     def run(self):
#         # threadLock.acquire()
#         print ("开启线程： " + self.name)
#         self.b_compute_similiar_button.update()
#         self.computer.compute(self, self.image_list, self.image_dir, self.threshold, self.listbox, self.logvar, self.log_label)
#         self.btnvar.set("compute similarity")
#         self.btn.update()
#         self.log_var.set("Summary: %d duplicate image pair founded"%self.ml_duplicates_listbox.size())
#         self.log_label.update()

#     def stop(self):
#         self.__running.clear()        # 设置为False    


class Similarity_Computer(object):
    
    def __init__(self, feature_type="sift"):
        
        self.feature_extractor = cv2.xfeatures2d.SURF_create()
        self.bfmatcher = cv2.BFMatcher(cv2.NORM_L2, True)
        self.running = False


    def _norm_score_(self, img1, img2):
        height1, width1, _ = img1.shape
        height2, width2, _ = img2.shape
        if (width1 * height1) < (width2 * height2):
            img2 = cv2.resize(img2, (width1, height1))
        else:
            img1 = cv2.resize(img1, (width2, height2))
        height, width, _ = img1.shape
        errorL2 = cv2.norm(img1, img2, cv2.NORM_L2)
        score = 1.0 - errorL2/float(width*height)
        return score

    def _dp_score_(self, dp1, dp2):
        matches = self.bfmatcher.match(dp1, dp2)
        if len(matches) > 0:
            distances = [match.distance for match in matches]
            if len(distances) == 0:
                score = 0.0
            else:
                score = 1.0 - np.mean(distances)
        else:
            score=0.0
        return score

    def compute(self, image_list, image_dir='./', threshold=0.8, listbox=None, logvar=None, log_label=None):
        self.running = True
        summary = len(image_list)
        starttime = datetime.datetime.now()
        dps_paths = []
        for idx, imgpath in enumerate(image_list): 
            image = cv2.imread(os.path.join(os.path.normpath(image_dir), os.path.normpath(imgpath)))
            _, dp = self.feature_extractor.detectAndCompute(image, None)
            dps_paths.append((dp, imgpath))
            if log_label is not None and logvar is not None:
                usedtime = datetime.datetime.now() - starttime
                needtime = usedtime / (idx+1) * (summary-idx-1)
                logvar.set("Feature extracting %.2f %% feature have computed. %.4f Secs have used, %.4f Secs still need." % ((idx+1)/summary*100.0, usedtime.total_seconds(), needtime.total_seconds()))
                log_label.update()
            if not self.running:
                return

        if log_label is not None and logvar is not None:
            logvar.set("Feature sorting...")
            log_label.update()
        dps_paths.sort(key=lambda d: 0 if d[0] is None else len(d[0]))

        summary = (len(image_list)-1) * len(image_list) / 2.0
        count = 0.0
        records = [0.0]
        for idx1, (dp1, imgpath1) in enumerate(dps_paths):
            if dp1 is None or len(dp1) == 0:
                image1 = cv2.imread(os.path.join(os.path.normpath(image_dir), os.path.normpath(imgpath1)))
            else:
                image1 = None
            for idx2 in range(idx1+1, len(dps_paths)):
                dp2, imgpath2 = dps_paths[idx2]
                if image1 is None and dp2 is not None and len(dp2) > 0:
                    score = self._dp_score_(dp1, dp2)
                else:
                    image2 = cv2.imread(os.path.join(os.path.normpath(image_dir), os.path.normpath(imgpath2)))
                    score = self._norm_score_(image1, image2)
                
                if score > threshold and listbox is not None:
                    for tmpidx, tmp in enumerate(records):
                        if score > tmp:
                            records.insert(tmpidx, score)
                            listbox.insert(tmpidx, (imgpath1, imgpath2, "%.2f %%"%(score*100)))
                            listbox.update()
                            break
                        else:
                            continue
                count += 1
                if log_label is not None and logvar is not None:
                    usedtime = datetime.datetime.now() - starttime
                    needtime = usedtime / count * (summary-count)
                    logvar.set("%.2f %% have computed, %d pairs of duplicate. %.4f Secs have been used, %.4f Secs still need." % (count/summary*100.0, listbox.size(), usedtime.total_seconds(), needtime.total_seconds()))
                    log_label.update()
                if not self.running:
                    return
        self.running = False
import numpy as np
import cv2


def process_image(filename):
    # raw_img = cv2.imread('static/images/'+ filename, cv2.IMREAD_GRAYSCALE)
    raw_img = cv2.imread('static/images/' + filename, cv2.IMREAD_GRAYSCALE)
    _, contours_raw, _ = cv2.findContours(raw_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    backtorgb_raw = cv2.cvtColor(raw_img,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(backtorgb_raw, contours_raw, -1, (255,255,0), 1)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    cl = clahe.apply(raw_img)
    ret, thresh_img = cv2.threshold(cl,150,255,cv2.THRESH_BINARY)
    ksize = 5
    kernel = np.ones((ksize,ksize), np.uint8)
    morph_img = cv2.morphologyEx(thresh_img, cv2.MORPH_ERODE, kernel)
    # ksize = 3
    # kernel = np.ones((ksize,ksize), np.uint8)
    # morph_img2 = cv2.morphologyEx(morph_img, cv2.MORPH_ERODE, kernel)
    _, contours, _ = cv2.findContours(morph_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    cont_img = cv2.cvtColor(raw_img,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(cont_img, contours, -1, (255,255,0), 1)
    centres = []
    centres_img = raw_img.copy()
    centres_img = cv2.cvtColor(centres_img, cv2.COLOR_GRAY2BGR)
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])
        if moments['m10'] != 0 and moments['m00'] != 0 and moments['m11'] != 0 and moments['m01'] != 0:
            centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
            cv2.circle(centres_img, centres[-1], 3, (255, 0, 0), -1)

    print(centres)

    for i in range(len(centres)):
        line_img = cv2.line(centres_img, (0, centres[i][1]), (centres[i][0],centres[i][1]), (255,255,0), 1)
        line_img = cv2.line(centres_img, (centres[i][0], 0), (centres[i][0],centres[i][1]), (255,255,0), 1)
        full_img = raw_img.copy()
        full_img = cv2.cvtColor(full_img, cv2.COLOR_GRAY2BGR)

    for centre in centres:
        cv2.circle(full_img, centre, 3, (255,0,0), -1)

    cv2.drawContours(full_img, contours, -1, (0,255,0), 1)

    for i in range(len(centres)):
        line_contour_img = cv2.line(full_img, (0, centres[i][1]), (centres[i][0],centres[i][1]), (255,255,0), 1)
        line_contour_img = cv2.line(full_img, (centres[i][0], 0), (centres[i][0],centres[i][1]), (255,255,0), 1)

    import operator
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    lineType = 2
    p = (5,10)
    height = full_img.shape[0]
    cm = 8
    pxl = height

    def pxl2cm(height_pxl):
        return cm*height_pxl/pxl

    cm_y = []
    for i in range(len(centres)) :
        cm_y.append(round(pxl2cm(centres[i][1]), 2))

    print(cm_y)
    full_img = raw_img.copy()
    full_img = cv2.cvtColor(full_img, cv2.COLOR_GRAY2BGR)
    count = 0

    for centre in centres:
        color = (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))
        cv2.putText(full_img, "{} cm".format(cm_y[count]), tuple(map(operator.add, centre, p)), font, fontScale, color, lineType)
        cv2.line(full_img, (0,centre[1]), centre, color, thickness=1)
        cv2.line(full_img, (centre[0],0), centre, color, thickness=1)
        cv2.circle(full_img, centre, 3, (255,0,0), -1)
        count+= 1

    cv2.drawContours(full_img, contours, -1, (0,255,0), 1)

    centres_np = np.array(centres)
    centres_sorted = centres_np[centres_np[:,0].argsort()[::-1]]
    centres_sorted

    dna_lanes = centres_sorted[0:6]
    reference_lanes = centres_sorted[6:]

    for center in dna_lanes:
        closest_reference_idx = (np.abs(reference_lanes[:,1]-center[1])).argmin()
        print(reference_lanes[closest_reference_idx])

    dna_lanes = centres_sorted[0:6]
    reference_lanes = centres_sorted[6:]

    user_input_example = [0, 130]
    closest_reference_idx = (np.abs(reference_lanes[:,1]-user_input_example[1])).argmin()
    reference_center = reference_lanes[closest_reference_idx]
    max_delta_px = 20
    ket = []
    print(reference_lanes)

    for center in dna_lanes:
        if np.abs(reference_center[1] - center[1]) <= max_delta_px:
            ket.append("Yes")
            print(True)
        else:
            ket.append("No")
            print(False)
    print(ket)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    lineType = 2
    n = (5,30)
    c=0

    for centre in dna_lanes:
        cv2.putText(full_img, "{}".format(ket[c]), tuple(map(operator.add, centre, n)), font, fontScale, (255,255,0), lineType)
        c += 1
    # final_filename = "processed_coba_coba.jpg"
    # cv2.imwrite('static/uploads/' + final_filename,full_img)
        final_filename = "processed_" + filename
        cv2.imwrite('static/uploads/' + final_filename,full_img)
        final_imgname = 'static/uploads/' + final_filename
    return(final_imgname)
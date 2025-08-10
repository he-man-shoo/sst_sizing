import math
from reportlab.lib.pagesizes import letter, A1, landscape
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import *
from datetime import date



def create_SLD(proj_location, proj_name, mv_vol, skid_kVA_at_max_temp, max_sst_per_skid, 
               solar_mw, number_skids_solar, solar_dc_vol, 
               storage_mw, number_skids_storage, storage_dc_vol, 
               dc_load_mw, number_skids_dc_load, load_dc_vol, 
               pcs_string, temp_string, ):

    def draw_arrow(c, x1, y1, x2, y2, arrow_size, orient):
        c.setDash()
        c.setLineWidth(0.4)

        if orient == 1:
            """
            Draw an arrow on the canvas from (start_x, start_y) to (end_x, end_y).
            arrow_size determines the size of the arrowhead.
            """

            # Draw the main line
            c.line(x1, y1, x2, y2)
            
            c.setFont("Helvetica", 14)
            c.drawCentredString(x1-2, y1-5, "//")


            # Draw the second arrowhead
            c.line(x2, y2, x2 - arrow_size, y2 + arrow_size/2)
            c.line(x2, y2, x2 - arrow_size, y2 - arrow_size/2)

            c.setFont("Helvetica", 14)


        if orient == 2:
            """
            Draw an arrow on the canvas from (start_x, start_y) to (end_x, end_y).
            arrow_size determines the size of the arrowhead.
            """

            # Draw the main line
            c.line(x1, y1, x2, y2)
            
            # Draw the second arrowhead
            c.line(x2, y2, x2 - arrow_size, y2 + arrow_size/2)
            c.line(x2, y2, x2 - arrow_size, y2 - arrow_size/2)

            c.setFont("Helvetica", 14)

        if orient == 3:
            """
            Draw an arrow on the canvas from (start_x, start_y) to (end_x, end_y).
            arrow_size determines the size of the arrowhead.
            """

            # Draw the main line
            c.line(x1, y1, x2, y2)
            
            # Draw the second arrowhead
            c.line(x1, y1, x1 + arrow_size, y1 + arrow_size/2)
            c.line(x1, y1, x1 + arrow_size, y1 - arrow_size/2)

            c.setFont("Helvetica", 14)
            # c.drawCentredString(x2+2, y2-5, "//")

        if orient == 4:
            """
            Draw an arrow on the canvas from (start_x, start_y) to (end_x, end_y).
            arrow_size determines the size of the arrowhead.
            """

            # Draw the main line
            c.line(x1, y1, x2, y2)
            
            # Draw the second arrowhead
            c.line(x1, y1, x2 + 1.5, y2-arrow_size/2)
            c.line(x1, y1, x2 + 4.5, y2 + arrow_size/20)

            c.setFont("Helvetica", 14)

        if orient == 5:
            """
            Draw an arrow on the canvas from (start_x, start_y) to (end_x, end_y).
            arrow_size determines the size of the arrowhead.
            """

            # Draw the main line
            c.line(x1, y1, x2, y2)
            
            # Draw the second arrowhead
            c.line(x1, y1, x2 + 3, y1 + arrow_size/2)
            c.line(x1, y1, x2 - 3, y1 + arrow_size/2)

            c.setFont("Helvetica", 14)
        c.setDash()
        c.setLineWidth(0.4)


    def border(c, feeder_type, rating):
        # Draw a rectangle
        c.setStrokeColorRGB(0, 0, 0)  # Set stroke color to black
        c.rect(20*mm, 20*mm, (841-40)*mm, (594-40)*mm, fill=0)  # (x, y, width, height)

        x_top_corner = (841-20)*mm
        y_top_corner = (594-20)*mm

        x_bot_corner = (841-20)*mm
        y_bot_corner = (20)*mm

        c.setFont("Helvetica", 14)

        c.rect(x_top_corner- 360, y_top_corner - 40, 360, 40, fill=0)  # (x, y, width, height)
        c.drawCentredString(x_top_corner - 180, y_top_corner - 25, "NOTES")

        c.setFont("Helvetica", 8)
        x_notes = x_top_corner - 350
        y_notes = y_top_corner - 60

        c.drawString(x_notes, y_notes,      " 1. THIS DINGLE LINE DIAGRAM IS FOR REFERENCE")
        
        c.drawString(x_notes, y_notes - 20, " 2. EQUIPMENT RATING SHOWN ARE NAMEPLATE VALUES.")
        
        c.drawString(x_notes, y_notes - 40, " 3. THIS DOCUMENT ONLY SHOWS EQUIPMENT IN HERON POWER'S SCOPE")
        c.drawString(x_notes, y_notes - 60, " 4. FINAL SITE LEVEL SLD IN BUYER'S SCOPE. AS REQUIRED, SITE LEVEL SLD TO ALSO")
        c.drawString(x_notes, y_notes - 70, "     INCLUDE EQUIPMENT OUTSIDE OF HERON POWER'S SCOPE INCLUDING BUT")
        c.drawString(x_notes, y_notes - 80, "     NOT LIMITED TO AUX TRANSFORMERS AND AC PANELS, AUGMENTATION EQUIPMENT")
        c.drawString(x_notes, y_notes - 90, "     REQUIRED OVER THE LIFE OF PROJECT, MV SWITCHGEAR, SUBSTATION YARD ETC.")

        c.rect(x_top_corner- 360, y_notes - 140, 360, 200, fill=0)

        c.setFont("Helvetica", 9)

        c.rect(x_bot_corner - 360, y_bot_corner, 360, 40, fill=0)  # (x, y, width, height)
        c.drawCentredString(x_bot_corner - 270, y_bot_corner + 15, "REASON FOR CONTROL - <>")
        c.drawCentredString(x_bot_corner - 90, y_bot_corner + 15, "DRAWING RELEASE DATE: " + str(date.today()))
        
        c.rect(x_bot_corner - 360, y_bot_corner + 40, 360, 40, fill=0)  # (x, y, width, height)
        c.drawCentredString(x_bot_corner - 270, y_bot_corner + 40 + 15, "SECURITY LEVEL - <>")
        c.drawCentredString(x_bot_corner - 90, y_bot_corner + 40 + 15, "EXPORT CLASSIFICATION - <>")

        c.rect(x_bot_corner - 360, y_bot_corner, 180, 80, fill=0)  # (x, y, width, height)


        c.rect(x_bot_corner - 360, y_bot_corner+80, 360, 160, fill=0)  # (x, y, width, height)

        c.setFont("Helvetica", 10)
        c.drawCentredString(x_bot_corner - 170, y_bot_corner + 225, "EXPORT ADMINISTRATION REGULATIONS WARNING")
        
        c.setFont("Helvetica", 8)
        c.drawString(x_bot_corner - 350, y_bot_corner + 210, "THIS DOCUMENT CONTAINS TECHNICAL DATA WHICH IF EXPORTED FROM THE UNITED")
        c.drawString(x_bot_corner - 350, y_bot_corner + 200, "STATES MUST BE EXPORTED IN ACCORDANCE WITH THE EXPORT ADMINISTRATION ")
        c.drawString(x_bot_corner - 350, y_bot_corner + 190, "REGULATIONS. DIVERSION CONTRARY TO U.S. LAW IS PROHIBITED.")

        c.setFont("Helvetica", 10)
        c.drawCentredString(x_bot_corner - 170, y_bot_corner + 155, "CONFIDENTIAL & PROPRIETARY")

        c.setFont("Helvetica", 8)
        c.drawString(x_bot_corner - 350, y_bot_corner + 140, "THIS DOCUMENT CONTAINS COMPANY CONFIDENTIAL AND PROPRIETARY")
        c.drawString(x_bot_corner - 350, y_bot_corner + 130, "INFORMATION OF HERON POWER.NEITHER THIS DOCUMENT, NOR ANY INFORMATION")
        c.drawString(x_bot_corner - 350, y_bot_corner + 120, "OBTAINED THEREFROM IS TO REPRODUCED,TRANSMITTED, OR DISCLOSED TO ANY")
        c.drawString(x_bot_corner - 350, y_bot_corner + 110, "THIRD-PARTY WITHOUT FIRST RECEIVING THE EXPRESS WRITTEN AUTHORIZATION OF")
        c.drawString(x_bot_corner - 350, y_bot_corner + 100, "HERON POWER.")

        c.drawString(x_bot_corner - 350, y_bot_corner + 90, "© HERON POWER, INC. ALL RIGHTS RESERVED")

        c.rect(x_bot_corner - 360, y_bot_corner+240, 360, 60, fill=0)  # (x, y, width, height)
        c.setFont("Helvetica", 18)
        c.drawCentredString(x_bot_corner - 180, y_bot_corner + 262, "PROJECT SINGLE LINE DIAGRAM")

        c.rect(x_bot_corner - 360, y_bot_corner+300, 360, 120, fill=0)  # (x, y, width, height)
        c.drawImage("logo.png", x_bot_corner - 270, y_bot_corner+320, height = 80, width = 180)

        c.rect(x_bot_corner - 360, y_bot_corner+420, 360, 80, fill=0)  # (x, y, width, height)
        c.setFont("Helvetica", 14)
        c.drawCentredString(x_bot_corner - 180, y_bot_corner + 440, proj_name + ", "+ proj_location)
        c.setFont("Helvetica", 18)

        if feeder_type == "SOLAR":
            c.drawCentredString(x_bot_corner - 180, y_bot_corner + 470, '{:,.2f}'.format(rating) + " MW SOLAR PLANT")
        if feeder_type == "BATTERY STORAGE":
            c.drawCentredString(x_bot_corner - 180, y_bot_corner + 470, '{:,.2f}'.format(rating) + " MW BESS")
        if feeder_type == "DC LOAD":
            c.drawCentredString(x_bot_corner - 180, y_bot_corner + 470, '{:,.2f}'.format(rating) + " MW DC LOADS")


        c.rect(x_bot_corner - 360, y_bot_corner+500, 360, 60, fill=0)  # (x, y, width, height)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x_bot_corner - 180, y_bot_corner + 522, "NOT FOR CONSTRUCTION")

        # c.setDash(6, 4)
        c.setLineWidth(2)
        c.line(x_bot_corner - 700, y_top_corner - 40, x_bot_corner - 700, y_bot_corner + 40)
        # c.drawString(x_bot_corner - 1020, y_top_corner - 50, "HERON POWER'S")
        # c.drawString(x_bot_corner - 1020, y_top_corner - 68, "SCOPE")    
        # c.drawString(x_bot_corner - 790, y_top_corner - 50, "BUYER'S SCOPE")

        c.setFont("Helvetica", 14)

        c.setDash()
        c.setLineWidth(0.4)




    def add_feeder(c, x, y, feeder_number, feeder_block_qty, dc_voltage, unique_feeder, feeder_type):
        y_feeder = y

        if feeder_block_qty == 0:

            c.setFont("Helvetica-Bold", 12)
            
            c.drawString(x + 1620, y+50, "FEEDER #" + str(feeder_number+1) + " TO MEDIUM VOLTAGE BUS")
            
            c.setFont("Helvetica-Oblique", 11)

            c.drawString(x + 1620, y+30, "SAME AS FEEDER #" + str(unique_feeder))

            draw_arrow(c, x + 1330, y + 50, x + 1600, y+50, 10, 1)

        else:
            c.setFont("Helvetica-Bold", 12)

            c.drawString(x + 1620, y+272, "FEEDER #" + str(feeder_number+1) + " TO MEDIUM VOLTAGE BUS")

            for i in range(feeder_block_qty):
                # Outer Rectangle
                c.setDash(6, 4)
                c.setLineWidth(0.4)

                x = x + (1500 - 180*feeder_block_qty)/(feeder_block_qty+1)
                c.rect(x, y_feeder, 180, 260)  # (x, y, width, height)

                c.setDash()
                c.setLineWidth(0.4)
                c.setFont("Helvetica", 8)
                c.drawString(x + 5, y_feeder - 10, str(feeder_type) + " F" + str(feeder_number+1) + " #" + str(i + 1))
                c.setFont("Helvetica-Bold", 14)

                x_block = x

                x = x_block + (180 - 20*4)/(4+1)
                y = y_feeder + 20

                x_mid = x_block + 180/2

                c.line(x_mid + 20, y + 260, x_mid + 20 + 180 - 20 + (1500 - 180*feeder_block_qty)/(feeder_block_qty+1), y + 260)

                c.setLineWidth(0.8)

                c.rect(x - 15, y + 55, 170, 177)  # (x, y, width, height)

                c.setDash()
                c.setLineWidth(0.4)
            
                if i == feeder_block_qty - 1:
                    draw_arrow(c, 1600, y + 260, 1700, y+260, 10, 2)
                if i == 0:
                    
                    # Ground
                    c.line(x_mid - 40, y + 260 - 10, x_mid - 40, y + 260 + 10)
                    c.line(x_mid - 45, y + 260 - 7, x_mid - 45, y + 260 + 7)
                    c.line(x_mid - 50, y + 260 - 4, x_mid - 50, y + 260 + 4)

                    c.line(x_mid, y + 260, x_mid - 40, y + 260)

                    # PCS SPECIFICATIONS
                    c.setFont("Helvetica", 6)
                    c.drawString(x_mid + 2, y + 160, "HERON LINK SKID")
                    c.drawString(x_mid + 2, y + 150, pcs_string)
                    c.drawString(x_mid + 2, y + 143, temp_string)

                    c.drawString(x_mid + 10, y + 125, str(mv_vol)+" KV AC")


                    c.drawCentredString(x_mid, y, str(dc_voltage[0]) +" V DC - " + str(dc_voltage[1]) +" V DC")

                    c.setFont("Helvetica-Bold", 14)
                    
                   
                for i in range(3):
                    # Ground
                    c.line(x_mid - 34, y + 240 - 20 - 35*i, x_mid - 34, y + 240 - 10 - 35*i)
                    c.line(x_mid - 37, y + 240 - 17 - 35*i, x_mid - 37, y + 240 - 13 - 35*i)
                    c.line(x_mid - 40, y + 240 - 16 - 35*i, x_mid - 40, y + 240 - 14 - 35*i)

                    c.line(x_mid - 34, y + 240 - 15 - 35*i, x_mid - 25, y + 240 - 15 - 35*i)
                    c.line(x_mid - 25, y + 240 - 15 - 35*i, x_mid - 25, y + 240 - 18 - 35*i)
                    
                    # Breaker
                    c.line(x_mid - 25, y + 240 - 18 - 35*i, x_mid - 20, y + 240 - 23 - 35*i)
                    c.line(x_mid - 25, y + 240 - 23 - 35*i, x_mid - 25, y + 240 - 30 - 35*i)
                    
                    c.line(x_mid - 25, y + 240 - 30 - 35*i, x_mid - 30, y + 240 - 30 - 35*i)
                    
                    # Breaker
                    c.line(x_mid - 30, y + 240 - 30 - 35*i, x_mid - 35, y + 240 - 25 - 35*i)
                    c.line(x_mid - 35, y + 240 - 30 - 35*i, x_mid - 50, y + 240 - 30 - 35*i)
                
                c.line(x_mid - 50, y + 240 - 30, x_mid - 50, y + 240 - 30 - 35*2)
                c.line(x_mid - 25, y + 240 - 30 - 35*2, x_mid, y + 240 - 30 - 35*2)
                
                c.line(x_mid + 20, y + 260, x_mid + 20, y + 240 - 30 - 35*1)
                c.line(x_mid + 20, y + 240 - 30 - 35*1, x_mid - 25, y + 240 - 30 - 35*1)
                
                c.line(x_mid, y + 240 - 30, x_mid, y + 260)
                c.line(x_mid, y + 240 - 30, x_mid - 25, y + 240 - 30)

                # After RMU
                c.line(x_mid, y + 120, x_mid, y + 140)

                y = y - 10

                # MV AC BUS #AC BUS LENGTH = 140
                c.line(x_mid-70, y + 130, x_mid+70, y + 130)

                # # Vertical Lines from AC Bus to SSTs
                for i in range (max_sst_per_skid):
                    link_center = x_mid-100 + 200/(max_sst_per_skid+1)*(i+1)
                    c.line(link_center, y + 110, link_center, y + 130)
                
                y = y - 10

                for i in range (max_sst_per_skid):

                    link_center = x_mid-100 + 200/(max_sst_per_skid+1)*(i+1)

                    # Medium Voltage Transformer
                    c.line(link_center-1, y + 90, link_center-1 , y + 110)
                    c.line(link_center+1, y + 90, link_center+1, y + 110)

                    for j in range(4):
                        c.arc(link_center - 9, (y + 92.5 + 5*j) + 2.5, link_center - 2, (y + 92.5 + 5*j) - 2.5, -90, 180)
                        c.arc(link_center + 9, (y + 92.5 + 5*j) + 2.5, link_center + 2, (y + 92.5 + 5*j) - 2.5, 90, 180)

                # SST Blocks

                # SST Width = 40; Length = 80

                    # Inverter Symbol
                    c.rect(link_center - 12.5, y + 80, 25, 40)  # (x, y, width, height)
                    c.line(link_center - 12.5, y + 80, link_center + 12.5, y + 120) # cross line

                    c.line(link_center + 7, y + 82, link_center + 11, y + 82) # DC Symbol
                    c.line(link_center + 7, y + 83, link_center + 11, y + 83) # DC Symbol
                    
                    c.arc(link_center - 7, y + 114, link_center - 9,  y + 118, 0, 180) # AC Symbol
                    c.arc(link_center - 7, y + 114, link_center - 5,  y + 118, 180, 180) # AC Symbol
                    
                    c.line(link_center, y + 60, link_center, y + 80) # DC Cable

                    if feeder_type == "SOLAR":
                        # Battery Symbol
                        c.circle(link_center, y + 45, 15)  # (x, y, radius)
                        # Calculate arrow positions (45-degree angles)
                        arrow_size = 10
                        radius = 15

                        # First arrow (top-left, 45 degrees)
                        start_x1 = link_center - radius * math.cos(math.radians(45))
                        start_y1 = y + 45 + radius * math.sin(math.radians(45))
                        end_x1 = link_center - (radius + arrow_size) * math.cos(math.radians(45))
                        end_y1 = y + 45 + (radius + arrow_size) * math.sin(math.radians(45))
                        draw_arrow(c, start_x1, start_y1, end_x1, end_y1, arrow_size, orient=4)
  

                        c.line(link_center - 10, y + 45, link_center - 2, y + 45)
                        c.line(link_center - 2, y + 42, link_center - 2, y + 48)

                        c.line(link_center + 10, y + 45, link_center + 2, y + 45)
                        c.line(link_center + 2, y + 40,  link_center + 2, y + 50)

                        c.setFont("Helvetica", 8)
                        c.drawString(link_center - 8, y + 50, "+")
                        c.drawString(link_center + 8, y + 50, "-")
                        c.setFont("Helvetica-Bold", 14)       

                    if feeder_type == "BATTERY STORAGE":
                        # Battery Symbol
                        c.rect(link_center - 15, y + 30, 30, 30)  # (x, y, width, height)
                        
                        c.line(link_center - 10, y + 45, link_center - 2, y + 45)
                        c.line(link_center - 2, y + 42, link_center - 2, y + 48)

                        c.line(link_center + 10, y + 45, link_center + 2, y + 45)
                        c.line(link_center + 2, y + 40,  link_center + 2, y + 50)

                        c.setFont("Helvetica", 8)
                        c.drawString(link_center - 10, y + 50, "+")
                        c.drawString(link_center + 10, y + 50, "-")
                        c.setFont("Helvetica-Bold", 14)       
                    
                    if feeder_type == "DC LOAD":
                        draw_arrow(c, link_center, y + 30, link_center, y + 60, 5, orient=5)



                # Battery Blocks
                x = x_block + 180


    
    
    pdf_path = f"{proj_name}, {proj_location} Single Line Diagram.pdf" 
    c = canvas.Canvas(pdf_path, pagesize=landscape(A1))

    total_feeder_number = 0
    
    def add_page(rating, number_skids, dc_voltage, skid_kVA_at_max_temp, mv_vol, pcs_string, temp_string, feeder_type, total_feeder_number):
            
            x_start = 100
            y_start = 1200

            x_start_block = x_start
            y_start_block = y_start

            x = x_start_block
            y = y_start_block

            block_qty = number_skids
            block_type = 1

            max_feeder_current = 900 #Amps
            safety_factor = 1.25 # 25%

            max_number_skids_per_feeder = math.floor(max_feeder_current*mv_vol*math.sqrt(3)/skid_kVA_at_max_temp/safety_factor)

            feeder_qty = math.ceil(block_qty/max_number_skids_per_feeder)

            feeders = []

            for i in range(feeder_qty):
                feeders.append(block_qty//feeder_qty)

            i = 0

            while sum(feeders) < block_qty:
                feeders[i] = feeders[i] + 1
                i = i + 1

            border(c, feeder_type, rating)
            unique_feeder = 0

            for i in range(len(feeders)):

                if i > 0 and feeders[i] == feeders[i-1]:
                    y = y + 220
                    add_feeder(c, x, y, i, 0, dc_voltage, unique_feeder, feeder_type)
                else:
                    add_feeder(c, x, y, i, feeders[i], dc_voltage, unique_feeder, feeder_type)
                    unique_feeder = i+1
                y = y - 300

                if y < 100 and i < len(feeders) - 1:
                    c.showPage()
                    border(c, feeder_type, rating)
                    y = y_start_block

            # Aux Feeder

            c.setFont("Helvetica-Bold", 11)

            c.drawString(x + 1620, y+50, "AUX FEEDER FROM MEDIUM VOLTAGE BUS")

            c.setFont("Helvetica-Oblique", 9)

            c.drawString(x + 1620, y+30, "480V AC CONNECTION REQUIRED TO SUPPLY AUX")
            
            draw_arrow(c, x + 1330, y + 50, x + 1600, y+50, 10, 3)

            c.setFont("Helvetica", 14)
    
    if solar_mw > 0:
        add_page(solar_mw, number_skids_solar, solar_dc_vol, skid_kVA_at_max_temp, mv_vol, pcs_string, temp_string, "SOLAR", total_feeder_number)
        c.showPage()  # Finalize the current page and start a new one    

    if storage_mw > 0:
        add_page(storage_mw, number_skids_storage, storage_dc_vol, skid_kVA_at_max_temp, mv_vol, pcs_string, temp_string, "BATTERY STORAGE", total_feeder_number)
        c.showPage()  # Finalize the current page and start a new one    

    if dc_load_mw > 0:
        add_page(dc_load_mw, number_skids_dc_load, load_dc_vol, skid_kVA_at_max_temp, mv_vol, pcs_string, temp_string, "DC LOAD", total_feeder_number)

    c.save()

    return pdf_path
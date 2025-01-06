/* import os

import vertexai

from vertexai.generative_models import GenerativeModel
*/
import IPython.display
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)

prompt8 = """ You are a professional copywriting assistant tasked with creating an "About Us" page for a merchant. The "About Us" page should follow a specific format based on the type of business the merchant represents. 

Your task involves:
1. **Using the format below** to identify key merchant details, including:
   - **Merchant Name**: The name of the business.
   - **Merchant Type**: The type of business (e.g., Beauty Salon, Spa, Boutique, etc.).
   - **Category: Services**: A list of services offered by the merchant.
   - **Category: Items**: A list of products or items the merchant sells.
    

2. **Follow the example structures** provided below based on the **merchant type**. Make sure to use the correct example (Beauty Salon, Boutique, Nail Spa, Massage parlor, Tattooing, Spa, etc.) for the merchant type provided in the input.

3. **Create the "About Us" page** based on the merchant details, ensuring it includes the following:
  
- Start with an introduction to the merchant by coming up with a mission, vision and value statement depending on the merchant type, categories, services and items of the merchant. Do not write the names of the categories, services or items in the mission statement. Do not use the word mission in the sentence. 
- Describe the services offered and what makes the salon unique. Do not write all the categories, services, item names but just highlight a couple of services and items to attract the attention of the customers. Format the names of services and items in the sentence.
- Include a brief information about the staff in the salon, experience, expertise
- Close with a friendly, inviting tone that encourages clients to visit or book an appointment.



4. **Use the format provided** to guide the output:
   - **Merchant Name**
   - **Merchant Type**
   - **Category: Services**
   - **Category: Items**
   
Note: Do not display the details in 4 as a raw information in the output.     
   
5. Your output should maintain a modern and  trendy tone, tailored to the specific merchant type, category and services. The output should not exceed more than 2500 characters  
— The output should have merchant name in Bold font

---
Example inputs are as follows:

##COMMENT: Prompt
##Comment: 1) The below prompt is very specific to Personal Service merchants (beauty and wellness). 2) The examples must be expanded to the Professional service merchant (Accounting, plumbing, home services, legal, etc). 


**Example 1: Beauty Salon (Radiance Beauty Lounge)**

#Input
Merchant Name: Radiance Beauty Lounge
Merchant Type: Beauty Salon
Category: Services
Hair Care:
Hair Styling
Hair Treatments
Skincare:
Deep Cleansing Facials
Anti-Aging Skin Treatments
Waxing & Grooming:
Full Body Waxing
Eyebrow Shaping
Makeup Services:
Professional Makeup Applications
Bridal & Special Occasion Makeup

Category: Items
Hair Products:
Premium Hair Care Products
Skincare Products:
Organic Skincare Products
Beauty Tools:
Makeup Brushes & Sponges
##Ourtput

Radiance Beauty Lounge, we belive in enhancing your natural beauty through exceptional services and personalized care. We believe that beauty is not just skin deep; it’s about confidence, self-care, and well-being.

Our team consists of passionate beauty professionals with years of experience in the industry. We offer a wide range of services, including hair styling, skincare, waxing, and makeup, all tailored to meet your specific needs. From the moment you step into our chic and cozy lounge, you’ll experience the warmth and expertise that sets us apart.

Indulge yourself with our luxury treatments and leave Radiance Beauty Lounge feeling refreshed, confident, and radiant.

---

**Example 2: Beauty Salon (Glam Room)**

##Input
Merchant Name: The Glam Room
Merchant Type: Beauty Salon
Category: Services
Hair Care:
Custom Haircuts
Hair Styling & Blowouts
Hair Coloring & Highlights
Makeup Services:
Professional Makeup Applications
Bridal & Event Makeup
Skincare:
Signature Facials
Anti-Aging Skin Treatments
Lash & Brow Enhancements:
Eyelash Extensions
Eyebrow Shaping

Category: Items
Hair Products:
Professional Hair Care Products
Makeup Products:
Glamorous Lipsticks & Eyeshadows
Makeup Brushes & Beauty Blenders
Skincare Products:
Luxury Facial Creams
Anti-Aging Serums

##Output

At The Glam Room, we believe that everyone deserves to feel glamorous every day. Our beauty studio is a sanctuary where our clients can escape the hustle and bustle of daily life and indulge in premium beauty services that leave them looking and feeling their absolute best.

The Glam Room was created by celebrity stylist Michelle Davis, who has over 15 years of experience in the beauty industry. Michelle’s vision was to build a space that blends luxury and accessibility, offering high-end services at prices that anyone can afford.

Our team is dedicated to staying on top of the latest beauty trends to ensure you always leave looking fabulous.

---

**Example 3: Spa (Pure Bliss Beauty)**


##Input

Merchant Name: Pure Bliss Beauty Spa
Merchant Type: Spa
Category: Services
Skincare:
Rejuvenating Facials
Anti-Aging Treatments
Body Care:
Body Scrubs & Wraps
Detox Treatments
Massages:
Relaxation Massages
Deep Tissue Massages
Nail Care:
Manicures & Pedicures
Specialized Treatments:
Advanced Skin Therapies
Customized Wellness Packages

Category: Items
Skincare Products:
Luxury Facial Creams
Organic Anti-Aging Serums
Body Care Products:
Exfoliating Body Scrubs
Hydrating Lotions
Gift Sets:
Spa & Wellness Gift Packages

##Output

Pure Bliss Beauty Spa is where luxury and relaxation meet. We are a full-service beauty salon offering a wide array of treatments designed to pamper and rejuvenate. Whether you need a quick refresh or an indulgent escape, we’ve got you covered.

Founded in 2012, Pure Bliss Beauty Spa was created to provide a tranquil oasis for people seeking to relax and look their best. Our expertly trained team is committed to delivering outstanding service and creating personalized beauty experiences tailored just for you.

At Pure Bliss, we use only the finest products and the latest technology to ensure your experience is nothing short of extraordinary.

---

**Example 4: Beauty Salon (Luxe Hair Studio)**

##Input

Merchant Name: Luxe Hair Studio
Merchant Type: Beauty Salon
Category: Services
Hair Care:
Custom Haircuts
Hair Styling
Hair Treatments
Skincare & Beauty:
Deep Cleansing Facials
Relaxing Spa Treatments
Category: Items
Hair Products:
Premium Hair Care Products
Skincare Products:
Organic Skincare Products

##Output

At Luxe Hair Studio, we believe every client deserves to feel beautiful, confident, and rejuvenated. Our passionate team of expert stylists and beauty professionals is dedicated to providing exceptional services in a relaxing, friendly environment. Whether you’re here for a quick trim, a bold new look, or a luxurious spa treatment, we promise to cater to your every need.

Luxe Hair Studio has become a leading destination for hair and beauty treatments. Our vision is simple: to combine cutting-edge techniques with the best beauty products available, ensuring every client leaves looking and feeling their best.

We can’t wait to welcome you to Luxe Hair Studio, where beauty meets elegance.
—

**Example 5: Massage Studio (Tranquil Touch Massage)**
##Input
Merchant Name: Tranquil Touch Massage
Merchant Type: Massage Studio
Category: Services
Massages:
Relaxation Massages
Deep Tissue Massages
Hot Stone Therapy
Aromatherapy Massage
Sports Massage
Specialized Treatments:
Prenatal Massage
Reflexology
Couples Massage
Category: Items
Massage Oils & Lotions:
Organic Lavender Massage Oil
Stress Relief Massage Lotion
Muscle Recovery Oil

##Output
At Tranquil Touch Massage, we believe that relaxation is a vital part of well-being. Our serene environment and expert massage therapists are here to provide a range of massages designed to leave you feeling relaxed, rejuvenated, and stress-free. Whether you need relief from chronic tension or just a moment of tranquility, we have the perfect treatment for you.
Founded with the vision to offer effective therapies in a peaceful, soothing atmosphere, Tranquil Touch Massage has become a go-to destination for individuals seeking stress relief, pain management, or a luxurious escape.
Our signature services, from deep tissue to aromatherapy massages, are designed to relax the body and calm the mind. Whether you're here for a quick escape or an extended session, our team is dedicated to providing the ultimate wellness experience.
Come visit us at Tranquil Touch Massage, where relaxation and healing begin.

**Example 6: Tattoo Studio (Ink Art Tattoo)**
##Input
Merchant Name: Ink Art Tattoo
Merchant Type: Tattoo Studio
Category: Services
Tattooing:
Custom Designs
Traditional Styles
Black & Grey Tattoos
Color Tattoos
Fine Line Tattoos
Piercings:
Ear Piercings
Nose Piercings
Lip Piercings
Category: Items
Tattoo Aftercare Products:
Tattoo Ointments
Healing Balms
Tattoo Moisturizers

##Output
Welcome to Ink Art Tattoo, where we specialize in turning your ideas into art. Whether you’re looking for a custom design or a traditional tattoo, our talented artists are here to create stunning pieces that you'll love for a lifetime. With a passion for ink and detail, Ink Art Tattoo is proud to be one of the most trusted studios for both experienced tattoo collectors and first-timers alike.
Our artists are trained in a variety of tattooing styles, including black & grey, color tattoos, and fine line work, ensuring every piece is personalized and professionally executed. Alongside our tattoo services, we also offer body piercing services to complement your style.
Ink Art Tattoo uses only the highest quality products, and our tattoo aftercare range helps keep your art looking vibrant and healthy. We are committed to providing a safe, comfortable, and clean environment for every client.
Come visit Ink Art Tattoo, where your next piece of art begins.
4o mini
You said:
Create one for Nail spa
ChatGPT said:
ChatGPT
**Example 7: Nail Spa (The Nail Loft)**
##Input
Merchant Name: The Nail Loft
Merchant Type: Nail Spa
Category: Services
Nail Care:
Manicures
Pedicures
Gel Manicures
Acrylic Nails
Nail Art & Design
Specialized Treatments:
Paraffin Wax Treatment
Hand & Foot Massages
Nail Strengthening Treatment
Category: Items
Nail Care Products:
Premium Nail Polishes
Nail Care Kits
Cuticle Oils
Nail Treatments & Serums

##Output
At The Nail Loft, we believe that every client deserves to experience the best in nail care. Our talented team of nail specialists is dedicated to providing luxurious treatments that leave your hands and feet feeling pampered and polished. Whether you're here for a quick manicure or a full spa treatment, we offer a variety of services to cater to your unique needs.
From gel manicures and acrylic nails to intricate nail art designs, The Nail Loft offers a wide range of nail care services that will make you feel both relaxed and beautiful. We also specialize in strengthening treatments and hand & foot massages to give you an all-encompassing, rejuvenating experience.
At The Nail Loft, we use only premium-quality products to ensure that your nails stay healthy and beautiful. Our nail care products, from cuticle oils to nail treatments, are carefully selected to enhance the beauty and longevity of your nails.
Visit The Nail Loft and indulge in the ultimate nail spa experience where beauty, relaxation, and care meet.
—
 
**Example 8: Face Painting Studio (Vivid Faces)**
##Input
Merchant Name: Vivid Faces
Merchant Type: Face Painting Studio
Category: Services
Face Painting:
Custom Designs
Themed Parties (e.g., Princess, Superheroes, Animals)
Glitter & Neon Art
Full Face Designs
Children’s Party Designs
Specialized Treatments:
Henna Designs
Body Painting
Airbrush Face Painting
Category: Items
Face Painting Kits:
Professional Paint Kits
Glitter & Stickers
Face Paint Brushes & Tools
Stencils for Designs

##Example Output is as follows: 
Welcome to Vivid Faces, where creativity and fun come to life through the art of face painting! Whether you’re looking to transform into your favorite character, add a splash of sparkle for a special event, or let your little one enjoy a colorful experience at a party, Vivid Faces has got you covered.
Our talented artists specialize in a variety of designs, from custom themes and full face art to glitter and neon designs that are perfect for festivals, birthdays, and other celebrations. Vivid Faces is dedicated to creating a fun, safe, and enjoyable environment for all ages, providing a personalized painting experience that will leave you glowing with joy.
We also offer specialized treatments such as henna and body painting, as well as airbrush face painting for those who want a more detailed, long-lasting design.
At Vivid Faces, we only use high-quality, non-toxic face paints and supplies to ensure the safety and comfort of our clients. Whether you're here for a festival, a party, or a special event, we promise a fun and vibrant experience.
Come visit us at Vivid Faces, where your imagination is brought to life with every brushstroke!

---------------------
Now, using the below merchant information, please generate a "About Us" page for the key details provided for a real merchant:"""

async def textpromptgeneration():


    print("I am being called")
    PROJECT_ID = "clover-dra-sandbox"  # @param {type: "string", placeholder: "[your-project-id]" isTemplate: true}

    LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    MODEL_ID = "gemini-1.5-pro"  # @param {type:"string"}

    model = GenerativeModel(MODEL_ID)   


    
   # example_model = GenerativeModel(
   # MODEL_ID,
   # system_instruction=[
   #     """ You are a highly skilled copywriting assistant, specialized in creating captivating "About Us" pages for businesses. Your task is to craft a compelling, professional, and customer-focused "About Us" description for a merchant based on the details provided.""",
   # ],
#)

# Set model parameters
    generation_parameters = GenerationConfig(
        temperature=0.9,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )
    mymodel = GenerativeModel(MODEL_ID, generation_config=generation_parameters) 
# Set safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }


    
    prompt = prompt8

# Set contents to send to the model
    contents = [prompt]

# Counts tokens
    #print(example_model.count_tokens(contents))

# Prompt the model to generate content
    
    response = await mymodel.generate_content_async(contents)
    #response = await example_model.generate_content_async(
            #contents,
            #generation_config=generation_config,
            #safety_settings=safety_settings,
    #)

#print(response.text)
    


# Print the model response
    print(f"\nAnswer:\n{response.text}")
#print(f'\nUsage metadata:\n{response.to_dict().get("usage_metadata")}')
#print(f"\nFinish reason:\n{response.candidates[0].finish_reason}")
#print(f"\nSafety settings:\n{response.candidates[0].safety_ratings}")
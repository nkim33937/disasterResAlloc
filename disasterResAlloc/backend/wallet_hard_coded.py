import sqlite3
from datetime import datetime
import asyncio

from ..components.wallet import create_multiple_wallets  # Adjust the import based on your project structure

async def main():
    """
    Main function to generate 9 wallet addresses and print their classic addresses.
    """
    # Generate 9 wallets
    wallets = await create_multiple_wallets(9)

    # Print the classic addresses
    for idx, wallet in enumerate(wallets, start=1):
        print(f"{wallet['classicAddress']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# async def generate_wallets():
#     """
#     Generates wallets and inserts their data into the 'organisation' table.
#     """

#     # List of organizations with their details
#     org_data = [
#         {
#             "name": "International Red Cross Honduras",
#             "location": "Honduras",
#             "email": "contact@redcross.hn",
#             "cause": "The International Red Cross in Honduras focuses on vector control and community health education to combat the spread of dengue. It also provides medical supplies and supports overwhelmed healthcare facilities.",
#             "disaster": "Dengue Outbreak",
#             "image": "https://www.icrc.org/sites/default/files/styles/desktop_full/public/document_new/image_plus_list/portada_honduras.jpg.webp?itok=1rRdfkzZ",
#         },
#         {
#             "name": "Palestine Children’s Relief Fund",
#             "location": "Gaza",
#             "email": "amnestygaza@gmail.com",
#             "cause": "PCRF specializes in offering medical care to children and families affected by the ongoing crisis. The organization focuses on providing urgent medical supplies, clean water, food, and long-term mental health support. PCRF also manages programs to help children in Gaza access specialized surgeries and healthcare unavailable locally.",
#             "disaster": "Genocide",
#             "image": "https://i.ytimg.com/vi/5-C1YnFQPOg/maxresdefault.jpg",
#         },
#         {
#             "name": "National Unit for Disaster Risk Management",
#             "location": "Colombia",
#             "email": "n/a",
#             "cause": "The National Unit for Disaster Risk Management (UNGRD) in Colombia coordinates evacuation plans and monitors volcanic activity to protect residents. It collaborates with the Geological Service of Colombia for early warning systems.",
#             "disaster": "Puracé Volcano",
#             "image": "https://i0.wp.com/www.thenonmad.com/wp-content/uploads/2018/03/Purace-31.jpg?fit=1600%2C1200&ssl=1",
#         },
#         {
#             "name": "Armenian Red Cross Society",
#             "location": "Armenia",
#             "email": "n/a",
#             "cause": "The Armenian Red Cross Society provides flood victims with essential supplies such as food, water, and shelter. It also runs community preparedness programs to mitigate future flood risks.",
#             "disaster": "Flash Floods",
#             "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyaeKFZag0kKt9FeLYtB7m0zBsQIKToW419w&s",
#         },
#         # Add the remaining organizations with their details...
#         {
#             "name": "BRAC",
#             "location": "Bangladesh",
#             "email": "n/a",
#             "cause": "BRAC supports displaced families by providing emergency shelters, food packages, and healthcare during tropical cyclones. They also run long-term recovery programs focused on rebuilding livelihoods.",
#             "disaster": "Tropical Cyclone Remal",
#             "image": "https://www.economist.com/img/b/1280/720/90/sites/default/files/images/2019/09/articles/main/20190907_irp003.jpg",
#         },
#         {
#             "name": "Bangladesh Red Crescent Society",
#             "location": "Bangladesh",
#             "email": "n/a",
#             "cause": "The Bangladesh Red Crescent Society offers medical assistance and disaster relief to cyclone-affected areas. It helps set up mobile clinics and works on restoring clean water supplies.",
#             "disaster": "Tropical Cyclone Remal",
#             "image": "https://redcross.eu/uploads/files/Latest%20News/EUAV%20Interview%20with%20Margherita/IMG_4.JPG",
#         },
#         {
#             "name": "UN World Food Programme",
#             "location": "Southern Africa",
#             "email": "n/a",
#             "cause": "The UN World Food Programme (WFP) addresses food insecurity caused by drought, distributing emergency food supplies and running nutrition programs to combat malnutrition.",
#             "disaster": "Drought",
#             "image": "https://www.wfp.org/sites/default/files/2024-03/WF121663_UGA_20200707_WFP-Hugh_Rutherford_5079.jpg",
#         },
#         {
#             "name": "Red Cross Botswana",
#             "location": "Botswana",
#             "email": "n/a",
#             "cause": "The Red Cross in Botswana provides drought-affected communities with water, food, and hygiene supplies. It also supports farmers with sustainable agricultural practices to build long-term resilience.",
#             "disaster": "Drought",
#             "image": "https://www.botswanaredcross.org.bw/images/2022/09/19/disaster-management.jpg",
#         },
#         {
#             "name": "Care International",
#             "location": "Multiple Locations",
#             "email": "n/a",
#             "cause": "Care International works globally to fight poverty and provide disaster relief, with programs focusing on emergency response, health, education, and economic development.",
#             "disaster": "Various",
#             "image": "https://www.care-international.org/sites/default/files/styles/gallery_image/public/2022-02/CI_Fistula_Sunday.jpg",
#         }
#     ]

#     # Generate wallets
#     wallets = await create_multiple_wallets(len(org_data))  # Ensure this function returns wallet objects with 'classicAddress' and optionally 'seed'

#     # Set 'amount' to 0 and assign organization details to each wallet
#     for wallet, org in zip(wallets, org_data):
#         wallet['amount'] = 0
#         wallet['name'] = org['name']
#         wallet['location'] = org['location']
#         wallet['email'] = org['email']
#         wallet['cause'] = org['cause']
#         wallet['disaster'] = org['disaster']
#         wallet['image'] = org['image']
#         # Set the 'created' date
#         wallet['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         # Include the 'seed' if it's part of the wallet data
#         wallet['seed'] = wallet.get('seed', None)

#     # Connect to your SQLite database
#     conn = sqlite3.connect('your_database.db')  # Replace with your actual database path
#     cursor = conn.cursor()

#     try:
#         # Insert each wallet into the 'organisation' table
#         for wallet in wallets:
#             cursor.execute("""
#                 INSERT INTO organisation (name, location, email, encoded_wallet, balance, created, seed, cause, disaster, image)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 wallet['name'],
#                 wallet['location'],
#                 wallet['email'],
#                 wallet['classicAddress'],
#                 wallet['amount'],
#                 wallet['created'],
#                 wallet['seed'],
#                 wallet['cause'],
#                 wallet['disaster'],
#                 wallet['image']
#             ))
#         # Commit the transaction
#         conn.commit()
#         print("Wallets have been inserted into the database.")
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         # Close the database connection
#         conn.close()

# if __name__ == "__main__":
#     asyncio.run(generate_wallets())


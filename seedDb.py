from createDb import Category, Item
from repository import Repository

db = Repository()

#When seeding the database removel all data to prevent creating duplicates.
db.deleteAllFromDatabase()

reiCategories = [Category(name='Camp & Hike'),  #1
                  Category(name='Climb'),       #2
                  Category(name='Cycle'),       #3
                  Category(name='Fitness'),     #4
                  Category(name='Paddle'),      #5
                  Category(name='Snowsports'),  #6
                  Category(name='Travel')]      #7
for category in reiCategories:
    db.addToDatabase(category)

reiItems = [Item(name='Big Agnes Chimney Creek 4 mtnGLO Tent', description= 'Winner of Backpacker magazine\'s 2015 Editors\' Choice Award for its built-in LED lighting, the 4-person Chimney Creek 4 mtnGLO Tent features ample living space, comfort and convenience.', categoryid=1),
Item(name='Osprey Aether 70 Pack', description='Slip on the Osprey Aether 70 pack and enjoy the comfort of a custom, heat-moldable hipbelt and a superb, lightweight design for enhanced load support on extended backcountry adventures.', categoryid=1),
Item(name='Marmot Trestles 30 Sleeping Bag - Women\'s - Long', description='Cold, damp weather calls for a synthetic insulated mummy bag. The women\'s Trestles 30 Sleeping Bag offers lofty warmth, low bulk and excellent packability, and continues to insulate even if wet.', categoryid=1),
Item(name='Hydro Flask Standard-Mouth Vacuum Water Bottle - 21 fl. oz.', description='The 21 fl. oz. Hydro Flask standard-mouth vacuum water bottle will be a faithful companion even on your busiest days. It\'s easy to carry and holds enough to keep you going without weighing you down.', categoryid=1),
Item(name='Black Diamond ReVolt Headlamp', description='Offering convenient power options, the low-profile Black Diamond ReVolt Headlamp lights your path with up to 130 lumens. It\'s also the first USB-rechargeable headlamp to also run on AAA batteries.', categoryid=1),
Item(name='Therm-a-Rest Single Slacker Hammock', description='Slack off in style with the Single Slacker Hammock from Therm - a- Rest. The single hammock stuffs into an attached pocket that doubles as a spot to stash a book while you relax.', categoryid=1),
Item(name='Big Agnes Double Z Air Sleeping Pad - Regular', description='Ultimate comfort should be available no matter where you rest your head, even on lightweight backpacking trips. Enter the Big Agnes Double Z Air Sleeping Pad, a 4 in. thick gateway to dreamland.', categoryid=1),
Item(name='MSR Talus TR-3 Trekking Poles', description='For mountaineering, backpacking and trekking, the MSR Talus TR-3 Trekking Poles are strong, lightweight and easy to adjust.', categoryid=1),
Item(name='CamelBak Fourteener 24 Hydration Pack - 3 Liters', description='The generously-sized CamelBak Fourteener 24 Hydration Pack is a compact and technical pack for done-in-a-day alpine adventures and everyday outings.', categoryid=1)]
for item in reiItems:
    db.addToDatabase(item)
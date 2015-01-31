#activate python
source triplex/backend/environment/bin/activate
#remove previous distributions
rm setup.py
rm -rf publishready/mac/build publishready/mac/dist
#create script and deploy new distrubution
py2applet --make-setup triplex/connector.py
python setup.py py2app
#move the distrubutions to their folder
mv build publishready/mac/build
mv dist publishready/mac/dist
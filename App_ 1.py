from flask import Flask, jsonify
import geopandas as gpd
import os

app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)))

# Load the shapefile
shapefile_path = r"D:\Azure\Api\Input\pincode_try.shp"
gdf = gpd.read_file(shapefile_path)
print(gdf)

@app.route('/all_data', methods=['GET'])
def get_all_data():
    df = gdf.drop(columns='geometry')
    data = df.to_dict('records')
    return jsonify(data)

@app.route('/states', methods=['GET'])
def get_states():
    states = gdf['STATE'].unique().tolist()
    return jsonify(states)

@app.route('/districts/<state>', methods=['GET'])
def get_districts(state):
    districts = gdf[gdf['STATE'] == state]['DISTRICT'].unique().tolist()
    return jsonify(districts)

@app.route('/tehsils/<state>/<district>', methods=['GET'])
def get_tehsils(state, district):
    tehsils = gdf[(gdf['STATE'] == state) & (gdf['DISTRICT'] == district)]['TEHSIL'].unique().tolist() 
    return jsonify(tehsils)

@app.route('/villages/<state>/<district>/<tehsil>', methods=['GET'])
def get_villages(state, district, tehsil):
    villages = gdf[(gdf['STATE'] == state) & (gdf['DISTRICT'] == district) & (gdf['TEHSIL'] == tehsil)]['VILLAGE'].unique().tolist()
    return jsonify(villages)

@app.route('/coordinates/<state>/<district>/<tehsil>/<village>', methods=['GET'])
def get_coordinates(state, district, tehsil, village):
    coords = gdf[(gdf['STATE'] == state) & (gdf['DISTRICT'] == district) & 
                 (gdf['TEHSIL'] == tehsil) & (gdf['VILLAGE'] == village)]['geometry'].apply(lambda geom: geom.centroid.coords[:]).tolist()
    return jsonify(coords)

# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=8000)
if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='localhost', port=8000)

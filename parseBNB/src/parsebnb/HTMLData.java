/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package parsebnb;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;

class HTMLData {
    private Integer Id;
    private String roomName;
    private JSONObject joInfo;
    private Map<String,Boolean> amenities;
    
    // tag - translation
    private Map<String,String> amenitiesTranslation;
    
    private Integer rating;
    private Map<String,Float> reviewSummary;
    private int min_nights;
    private int personCapacity;
    private String address;
    
    public HTMLData(String path) throws FileNotFoundException, IOException{
        String js= FileUtils.readFileToString(new File(path+"html.json"));
        this.joInfo = new JSONObject(js).getJSONObject("bootstrapData").getJSONObject("reduxData").getJSONObject("homePDP").getJSONObject("listingInfo").getJSONObject("listing");
        getRoomName();
        getAmenities();
        getRating();
        getReviewSummary();
        getMinNights();
        getPersonCapacity();
        getAddress();
//        echoAll();

    }
    private void echoAll(){
        System.out.println(this.Id);
        System.out.println(this.amenities);
        System.out.println(this.amenitiesTranslation);
        System.out.println(this.rating);
        System.out.println(this.reviewSummary);
        System.out.println(this.roomName);
        
    }
    
//    private void 
    
    private void getAddress(){
        if (joInfo.has("p3_summary_address"))
            this.address = joInfo.getString("p3_summary_address");
        else
            this.address = null;
    }
    private void getPersonCapacity(){
        this.personCapacity = joInfo.getInt("person_capacity");
    }
    
    private void getMinNights(){
        this.min_nights = joInfo.getInt("min_nights"); 
    }
    
    private void getRoomName() throws FileNotFoundException{
        this.roomName = joInfo.getString("name");
    }
    
    private void getAmenities(){
        this.amenities = new HashMap<String,Boolean>();
        this.amenitiesTranslation = new HashMap<String,String>();
        JSONArray amenities = joInfo.getJSONArray("listing_amenities");
        Integer i, length = amenities.length();
        for (i = 0; i < length; i++){
            this.amenities.put(amenities.getJSONObject(i).getString("tag"), amenities.getJSONObject(i).getBoolean("is_present"));
            this.amenitiesTranslation.put(amenities.getJSONObject(i).getString("tag"), amenities.getJSONObject(i).getString("name"));
        }
    }

    private void getRating(){
        this.rating = joInfo.getInt("star_rating");
    }
    
    private void getReviewSummary(){
        this.reviewSummary = new HashMap<String,Float>();
        String category;
        Float rating;
        JSONArray reviewArray = joInfo.getJSONObject("review_details_interface").getJSONArray("review_summary");
        Integer i, length =reviewArray.length();
        for (i = 0; i < length; i++){
            category = reviewArray.getJSONObject(i).getString("category");
            rating = Float.parseFloat(reviewArray.getJSONObject(i).getString("localized_rating"));
            this.reviewSummary.put(category, rating);
        }
    }
}

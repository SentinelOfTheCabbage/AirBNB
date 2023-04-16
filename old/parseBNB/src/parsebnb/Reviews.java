package parsebnb;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;

class Reviews {
    
    private JSONArray joInfo;
    private List<String> reviewerName = new ArrayList<String>();
    private List<String> createAt = new ArrayList<String>();
    private List<String> comment = new ArrayList<String>();
    private List<Integer> rating = new ArrayList<Integer>();
    private List<String> language = new ArrayList<String>();
    
    public Reviews(String path) throws IOException {
        String js= FileUtils.readFileToString(new File(path+"reviews.json"));
        this.joInfo = new JSONObject(js).getJSONArray("reviews");
        Integer i, length = joInfo.length();
        for (i = 0; i < length; i++){
            this.reviewerName.add(this.joInfo.getJSONObject(i).getJSONObject("reviewer").getString("first_name"));
            this.createAt.add(this.joInfo.getJSONObject(i).getString("created_at"));
            this.comment.add(this.joInfo.getJSONObject(i).getString("comments"));
            this.rating.add(this.joInfo.getJSONObject(i).getInt("rating"));
            
            if (this.joInfo.getJSONObject(i).has("language"))
                this.language.add(this.joInfo.getJSONObject(i).getString("language"));
            else
                this.language.add(null);
        }
//        echoExample(0);
    }
    private void echoExample(Integer count){
        Integer i, length;
        if (count == 0)
            length = this.reviewerName.size();
        else if (count < this.reviewerName.size()) 
            length = count;
        else
            length = this.reviewerName.size();
        
        for (i = 0;i < length; i++){
            System.out.println(this.reviewerName.get(i));
            System.out.println(this.createAt.get(i));
            System.out.println(this.comment.get(i));
            System.out.println(this.rating.get(i));
        }
            
    }
    
}

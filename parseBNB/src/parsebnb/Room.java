package parsebnb;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader; 
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator; 
import java.util.List;
import java.util.Map; 
import java.util.ArrayList;
import org.apache.commons.io.FileUtils;

import org.json.JSONArray; 
import org.json.JSONObject; 

class Room {
    private Integer Id;
    private String path;
    public HTMLData dataFromHtml;
    public Reviews reviewList;
    
    public Room(String path, Integer id) throws FileNotFoundException, IOException{
        this.Id = id;
        this.path = path+"/"+id.toString()+"/";
        this.dataFromHtml= new HTMLData(this.path);
        this.reviewList = new Reviews(this.path);
        
    }
}


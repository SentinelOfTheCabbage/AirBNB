package parsebnb;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader; 
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator; 
import java.util.List;
import java.util.Map; 
import org.apache.commons.io.FileUtils;
  
import org.json.JSONArray; 
import org.json.JSONObject; 
 
public class ParseBNB {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        ParseSettings options = new ParseSettings();
        String path = options.country+"/"+options.city+"/";
        String js= FileUtils.readFileToString(new File(path+"id_list.json"));
        JSONArray jo =  new JSONArray(js);
        Integer i,length = jo.length();
        System.out.println(length);
        List<Room> RoomList = new ArrayList<Room>();
        
        for (i = 0; i < length; i++){
            Room newElement = new Room(path, jo.getInt(i));
        }
    }
    
}

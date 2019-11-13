package Model;

import com.google.gson.annotations.SerializedName;

public class Tweet {

    private long id;
    private String text;
    private String lang;
    private User user;

    @SerializedName("retweet_count")
    private int retweetCount;

    @SerializedName("favorite_count")
    private int favoriteCount;

    //Constructor
    //Getters and Setters
    // Override toString()
}

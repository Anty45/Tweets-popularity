package KafkaProducer;

import Properties.TwitterProperties;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Client;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;


public class TwitterKafkaProducer {

    private static final Authentication authentication = new OAuth1(

            TwitterProperties.APIKey,
            TwitterProperties.APISecretKey,
            TwitterProperties.AccessToken,
            TwitterProperties.AccessTokenSecret);

    // track the terms of your choice. here im only tracking #bigdata.
    private StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint().trackTerms(TwitterProperties.HASHTAG);

    private BlockingQueue<String> queue = new LinkedBlockingQueue<>(10000);

    Client client = new ClientBuilder()
            .hosts(Constants.STREAM_HOST)
            .authentication(authentication)
            .endpoint(endpoint)
            .processor(new StringDelimitedProcessor(queue))
            .build();
}

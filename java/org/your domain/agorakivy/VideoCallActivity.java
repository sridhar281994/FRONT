package org.yourdomain.agorakivy;
import android.app.Activity;
import android.os.Bundle;
import android.widget.FrameLayout;
import io.agora.rtc2.RtcEngine;
import io.agora.rtc2.video.VideoCanvas;
import io.agora.rtc2.video.VideoEncoderConfiguration;
import io.agora.rtc2.Constants;
public class VideoCallActivity extends Activity {
    private RtcEngine mRtcEngine;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        FrameLayout container = new FrameLayout(this);
        setContentView(container);
        String appId = "YOUR_AGORA_APP_ID"; // replace this at runtime or hardcode
        String channel = getIntent().getStringExtra("channel");
        String token = getIntent().getStringExtra("token");
        try {
            mRtcEngine = RtcEngine.create(getBaseContext(), appId, null);
        } catch (Exception e) {
            e.printStackTrace();
        }
        mRtcEngine.enableVideo();
        mRtcEngine.setChannelProfile(Constants.CHANNEL_PROFILE_COMMUNICATION);
        mRtcEngine.setupLocalVideo(new VideoCanvas(0, VideoCanvas.RENDER_MODE_HIDDEN, container));
        mRtcEngine.startPreview();
        mRtcEngine.joinChannel(token, channel, "", 0);
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mRtcEngine != null) {
            mRtcEngine.leaveChannel();
            RtcEngine.destroy();
        }
    }
}





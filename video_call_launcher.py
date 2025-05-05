from jnius import autoclass
from android import activity


def launch_video_call(channel, token):
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    String = autoclass('java.lang.String')
    context = PythonActivity.mActivity
    VideoCallActivity = autoclass('org.yourdomain.agorakivy.VideoCallActivity')
    intent = Intent(context, VideoCallActivity)
    intent.putExtra("channel", String(channel))
    intent.putExtra("token", String(token))
    context.startActivity(intent)

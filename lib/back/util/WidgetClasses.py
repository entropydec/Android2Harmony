class WidgetClasses:
    widget_list = [
        'android.app.ActionBar$Tab',
        'android.support.v4.view.ViewPager',
        'android.support.v4.widget.DrawerLayout',
        'android.support.v7.app.ActionBar$Tab',
        'android.support.v7.app.ActionBar$b',
        'android.support.v7.widget.LinearLayoutCompat',
        'android.support.v7.widget.RecyclerView',
        'android.view.View',
        'android.webkit.WebView',
        'android.widget.AdapterView',
        'android.widget.Button',
        'android.widget.CheckBox',
        'android.widget.CheckedTextView',
        'android.widget.CompoundButton',
        'android.widget.DatePicker',
        'android.widget.EditText',
        'android.widget.ExpandableListView',
        'android.widget.FrameLayout',
        'android.widget.Gallery',
        'android.widget.GridView',
        'android.widget.HorizontalScrollView',
        'android.widget.Image',
        'android.widget.ImageButton',
        'android.widget.ImageView',
        'android.widget.LinearLayout',
        'android.widget.ListView',
        'android.widget.MultiAutoCompleteTextView',
        'android.widget.NumberPicker',
        'android.widget.ProgressBar',
        'android.widget.RadioButton',
        'android.widget.RatingBar',
        'android.widget.RelativeLayout',
        'android.widget.ScrollView',
        'android.widget.SearchView',
        'android.widget.SeekBar',
        'android.widget.Spinner',
        'android.widget.Switch',
        'android.widget.TabHost',
        'android.widget.TabWidget',
        'android.widget.TextView',
        'android.widget.TimePicker',
        'android.widget.ToggleButton',
        'android.widget.VideoView',
        'android.widget.ViewAnimator',
        'android.widget.ViewFlipper',
        'androidx.recyclerview.widget.RecyclerView',
        'androidx.viewpager.widget.ViewPager',
        'com.android.inputmethod.keyboard.Key'
    ]

    @classmethod
    def list(cls):
        return cls.widget_list


if __name__ == '__main__':
    widget_class_list = []
    f = open('/Users/xuhao/Downloads/test/widget_classes.txt', 'r')
    for line in f.readlines():
        widget_class_list.append(line.strip('\n'))
    for widget_class in widget_class_list:
        print(widget_class)

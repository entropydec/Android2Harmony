class Action:
    # action type
    click = "click"
    editText = "edit"
    longClick = "clickLong"
    swipeDown = 'swipe(down)'
    swipeUp = 'swipe(up)'
    swipeLeft = 'swipe(left)'
    swipeRight = 'swipe(right)'
    rotationUpSideDown = 'rotation(upsidedown)'
    rotationNatural = 'rotation(natural)'
    rotationLeft = 'rotation(left)'
    rotationRight = 'rotation(right)'

    # system action type
    menu = 'menu'
    back = 'back'
    home = 'home'
    launch = 'launch'
    stop = 'stop'

    def __init__(self, action_id, action_type, trigger_identify, weight=-1):
        self.action_id = action_id
        self.action_type = action_type
        self.trigger_identify = trigger_identify
        self.weight = weight

    def __lt__(self, other):
        return other.weight < self.weight

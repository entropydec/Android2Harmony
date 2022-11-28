import numpy as np
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from hashlib import md5
import logging
import xml.etree.ElementTree as ET
import logging
from util.WidgetClasses import WidgetClasses


class VectorsExtractor:
    recycle_classes = ['RecyclerView', 'ListView', 'GridView']
    widget_class_list = WidgetClasses.list()
    """
    抽取状态的特征向量
    """
    @classmethod
    def extract_vectors_from_layout(cls, layout):
        tree = ET.fromstring(layout)
        cls.delete_system_node(tree)
        vectors = []
        cls.preorder_traverse(vectors, tree)
        vectors = cls.split_and_zero_padding([vectors], 100)
        return vectors

    @classmethod
    def delete_system_node(cls, root):
        for child in list(root):
            if child.get('package') == 'com.android.systemui' and (
                    child.get('class') == 'android.widget.LinearLayout'
                    or child.get('class') == 'android.widget.FrameLayout'):
                root.remove(child)

    @classmethod
    def remove_recycle_items(cls, root):
        is_recycle = False
        if root.tag == 'node':
            for recycle_class in cls.recycle_classes:
                if recycle_class in root.get('class'):
                    is_recycle = True
                    break
        if not is_recycle:
            for child in list(root):
                cls.remove_recycle_items(child)
        else:
            view_classes = []
            for child in list(root):
                if child.get('class') in view_classes:
                    root.remove(child)
                else:
                    view_classes.append(child.get('class'))



    @classmethod
    def preorder_traverse(cls, vectors, node):
        if 'hierarchy' != node.tag:
            vector = cls.extract_vector_from_node(node)
            vectors.append(vector)

        for child in node:
            cls.preorder_traverse(vectors, child)

    @classmethod
    def split_and_zero_padding(cls, df, max_seq_length):
        return pad_sequences(df, padding='pre', truncating='post', maxlen=max_seq_length, dtype='float', value=0.0)

    @classmethod
    def extract_vector_from_node(cls, node):
        node_vector = [0.0] * (1 + 4 + len(cls.widget_class_list) + 1 + 40 * 4)
        # resolve NAF attribute
        if node.get('NAF') == '' or not node.get('NAF'):
            node_vector[0] = 0.0
        elif node.get('NAF') == 'true':
            node_vector[0] = 1.0

        # resolve bounds attribute
        bounds_string = node.get('bounds')
        if bounds_string == '' or not bounds_string:
            # print(node)
            node_vector[1] = 0.0
            node_vector[2] = 0.0
            node_vector[3] = 0.0
            node_vector[4] = 0.0
        else:
            lt_bounds_string = bounds_string[0: bounds_string.rfind('[')]
            rb_bounds_string = bounds_string[bounds_string.rfind('['): len(bounds_string)]
            lt_x = int(lt_bounds_string[1: lt_bounds_string.find(',')])
            lt_y = int(lt_bounds_string[lt_bounds_string.find(',') + 1: lt_bounds_string.rfind(']')])
            rb_x = int(rb_bounds_string[1: rb_bounds_string.find(',')])
            rb_y = int(rb_bounds_string[rb_bounds_string.find(',') + 1: rb_bounds_string.rfind(']')])
            # print('lt_x = ' + str(lt_x) + ' lt_y = ' + str(lt_y) + ' rb_x = ' + str(rb_x) + ' rb_y = ' + str(rb_y))
            node_vector[1] = round(lt_x / self.SCREEN_RESOLUTION_X, 2)
            node_vector[2] = round(lt_y / self.SCREEN_RESOLUTION_Y, 2)
            node_vector[3] = round(rb_x / self.SCREEN_RESOLUTION_X, 2)
            node_vector[4] = round(rb_y / self.SCREEN_RESOLUTION_Y, 2)

        # resolve class attribute
        widget_class = node.get('class')
        one_hot_num = 0
        for i in range(0, len(self.widget_class_list)):
            if self.widget_class_list[i] == widget_class:
                one_hot_num = i
                break
        if widget_class == self.widget_class_list[one_hot_num]:
            node_vector[one_hot_num + 5] = 1.0
        else:
            # logging.info(widget_class)
            node_vector[len(self.widget_class_list) + 5] = 1.0

        # resolve content-desc, len(self.widget_class_list) + 6 : len(self.widget_class_list) + 45
        # hash the string to 10 bits
        content_desc = node.get('content-desc')
        md5_str_16 = str(md5(content_desc.encode('utf-8')).hexdigest())
        md5_str_10 = str((int(md5_str_16, 16)))
        if len(md5_str_10) > 40:
            logging.error('length is beyond 40')
        for i in range(0, len(md5_str_10)):
            node_vector[len(self.widget_class_list) + 6 + i] = float(md5_str_10[i]) / 10
            # print(node_vector[len(self.widget_class_list) + 6 + i])
            if i >= 39:
                break

        # resolve package, len(self.widget_class_list) + 46 : len(self.widget_class_list) + 85
        package = node.get('package')
        md5_str_16 = str(md5(package.encode('utf-8')).hexdigest())
        md5_str_10 = str(int(md5_str_16, 16))
        if len(md5_str_10) > 40:
            logging.error('length is beyond 40')
        for i in range(0, len(md5_str_10)):
            node_vector[len(self.widget_class_list) + 46 + i] = float(md5_str_10[i]) / 10
            # print(node_vector[len(self.widget_class_list) + 6 + i])
            if i >= 39:
                break

        # resolve resource-id, len(self.widget_class_list) + 86 : len(self.widget_class_list) + 125
        resource_id = node.get('resource-id')
        md5_str_16 = str(md5(resource_id.encode('utf-8')).hexdigest())
        md5_str_10 = str(int(md5_str_16, 16))
        if len(md5_str_10) > 40:
            logging.error('length is beyond 40')
        for i in range(0, len(md5_str_10)):
            node_vector[len(self.widget_class_list) + 86 + i] = float(md5_str_10[i]) / 10
            if i >= 39:
                break

        # resolve text, len(self.widget_class_list) + 126 : len(self.widget_class_list) + 165
        text = node.get('text')
        md5_str_16 = str(md5(text.encode('utf-8')).hexdigest())
        md5_str_10 = str(int(md5_str_16, 16))
        if len(md5_str_10) > 40:
            logging.error('length is beyond 40')
        for i in range(0, len(md5_str_10)):
            node_vector[len(self.widget_class_list) + 126 + i] = float(md5_str_10[i]) / 10
            if i >= 39:
                break
        return node_vector

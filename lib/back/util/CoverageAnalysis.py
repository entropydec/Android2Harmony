#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 9:12 PM
# @Author  : Huang An

import os
import shutil
import xml
import xml.dom.minidom
import re
import collections
from util.Commander import Commander
import subprocess
from util.FileHelper import FileHelper


class CoverageAnalysis:

    def __init__(self, user_id, app_id, task_id, time_interval=30):
        self.manifest_file = FileHelper.manifest_file(app_id)
        self.app_source_path = FileHelper.source_code_dir(app_id)
        self.output_path = FileHelper.coverage_output_dir(user_id, task_id)
        self.report_path = FileHelper.coverage_report_dir(user_id, task_id)
        self.temp_path = FileHelper.coverage_temp_dir(user_id, task_id)
        self.time_interval = time_interval
        self.max_file_id = 0

    def output_coverage_report(self, result):
        file_list = os.listdir(self.output_path)
        # 存在覆盖度文件才进行分析
        if file_list:
            instruction_data, branch_data, cxty_data, line_data, method_data, class_data, activity_data = \
                self.get_curve_data(file_list)
            result.set_instruction_coverage(instruction_data['final'])
            result.set_branch_coverage(branch_data['final'])
            result.set_cxty_coverage(cxty_data['final'])
            result.set_line_coverage(line_data['final'])
            result.set_method_coverage(method_data['final'])
            result.set_class_coverage(class_data['final'])
            result.set_activity_coverage(activity_data['final'])
            self.save_curve_data(instruction_data, branch_data, cxty_data, line_data,
                                 method_data, class_data, activity_data)
        else:
            for k in result.coverage:
                result.coverage[k] = 0

    # 产生测试报告
    def generate_test_report(self, coverage_file_path):
        os.chdir(self.app_source_path)
        cmd = Commander.coverage_test_report(coverage_file_path)
        subprocess.run(cmd, shell=True, universal_newlines=True,
                       stdout=subprocess.PIPE)

    def get_coverage_data(self):
        instruction_coverage = 0.0
        branch_coverage = 0.0
        cxty_coverage = 0.0
        line_coverage = 0.0
        method_coverage = 0.0
        class_coverage = 0.0
        activity_coverage = 0.0
        file_path = os.path.join(self.app_source_path, 'build', 'reports', 'jacoco',
                                 'jacocoTestReportMergeWithParameter', 'jacocoTestReportMergeWithParameter.xml')
        dom = xml.dom.minidom.parse(file_path)
        root = dom.documentElement
        children = root.childNodes
        # get coverage information from counters
        for counter in children:
            if counter.getAttribute('type') == 'INSTRUCTION':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                instruction_coverage = float(covered) / (float(missed + covered))
            if counter.getAttribute('type') == 'BRANCH':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                branch_coverage = float(covered) / (float(missed + covered))
            if counter.getAttribute('type') == 'LINE':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                line_coverage = float(covered) / (float(missed + covered))
            if counter.getAttribute('type') == 'COMPLEXITY':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                cxty_coverage = float(covered) / (float(missed + covered))
            if counter.getAttribute('type') == 'METHOD':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                method_coverage = float(covered) / (float(missed + covered))
            if counter.getAttribute('type') == 'CLASS':
                missed = int(counter.getAttribute('missed'))
                covered = int(counter.getAttribute('covered'))
                class_coverage = float(covered) / (float(missed + covered))

        # get activity names from manifest
        activity_names = []
        covered_activity_num = 0
        manifest_file = ''
        if self.manifest_file == '':
            manifest_file = os.path.join(self.app_source_path, 'app', 'src', 'main', 'AndroidManifest.xml')
        else:
            manifest_file = os.path.join(self.app_source_path, self.manifest_file)
        manifest_dom = xml.dom.minidom.parse(self.manifest_file)
        manifest_root = manifest_dom.documentElement
        application_node = manifest_root.getElementsByTagName('application')[0]
        activity_nodes = application_node.getElementsByTagName('activity')
        for activity_node in activity_nodes:
            name_str = activity_node.getAttribute('android:name')
            name_strs = name_str.split('.')
            activity_name = name_strs[len(name_strs) - 1]
            print('activity name: ' + activity_name)
            activity_names.append(activity_name)

        # get activity coverage
        package_nodes = root.getElementsByTagName('package')
        for package_node in package_nodes:
            class_nodes = package_node.getElementsByTagName('class')
            for class_node in class_nodes:
                class_name_str = class_node.getAttribute('name')
                name_strs = class_name_str.split('/')
                class_name = name_strs[len(name_strs) - 1]
                if class_name in activity_names:
                    print('class name: ' + class_name)
                    for counter in class_node.childNodes:
                        if counter.getAttribute('type') == 'CLASS':
                            if int(counter.getAttribute('covered')) > 0:
                                print('covered')
                                covered_activity_num += 1
                            else:
                                print('not covered')

        activity_coverage = float(covered_activity_num) / float(len(activity_names))

        return instruction_coverage, branch_coverage, cxty_coverage, line_coverage, method_coverage, class_coverage, activity_coverage

    def get_curve_data(self, file_list):
        #
        instruction_coverage_data = {}
        branch_coverage_data = {}
        cxty_coverage_data = {}
        line_coverage_data = {}
        method_coverage_data = {}
        class_coverage_data = {}
        activity_coverage_data = {}

        # sort file with created time
        # file_list = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(target_coverage_file, x)))
        file_list.sort(key=lambda f: os.path.getctime(os.path.join(self.output_path, f)))
        for f in file_list:
            print('file_name: ' + f + ' created time: ' + str(
                os.path.getctime(os.path.join(self.output_path, f))))

        for f in file_list:

            if '.log' in f:
                continue
            if '.DS_Store' in f:
                continue

            if not os.path.exists(self.temp_path):
                os.makedirs(self.temp_path)
            # 每次从原始覆盖度文件夹target_coverage_file中移动一个ec文件到 NEW_COVERAGE_FILE
            shutil.copy2(os.path.join(self.output_path, f), self.temp_path)

            # 然后在NEW_COVERAGE_FILE统计覆盖度。
            self.generate_test_report(self.temp_path)

            instruction_coverage, branch_coverage, cxty_coverage, line_coverage, method_coverage, class_coverage, activity_coverage = self.get_coverage_data()
            pattern = re.compile("coverage_curve_(\S+).ec")
            file_id = re.findall(pattern, f)[0]

            # 下面这些dic是用来存放覆盖度信息的，比如instruction_coverage_data就是存放指令覆盖度信息的。
            # 可以看到是用int(file_id)作为索引，比如统计到coverage_curve_1.ec这个文件，那么file_id就是1。
            # 然后instruction_coverage_data[1]就是统计到coverage_curve_1.ec这个文件的覆盖度，
            # instruction_coverage_data[2]就是统计了coverage_curve_1.ec， coverage_curve_2.ec这两个文件的覆盖度，以此类推。

            instruction_coverage_data[int(file_id)] = instruction_coverage
            branch_coverage_data[int(file_id)] = branch_coverage
            cxty_coverage_data[int(file_id)] = cxty_coverage
            line_coverage_data[int(file_id)] = line_coverage
            method_coverage_data[int(file_id)] = method_coverage
            class_coverage_data[int(file_id)] = class_coverage
            activity_coverage_data[int(file_id)] = activity_coverage
            # MAX_ID就是统计一共有多少个ec文件，在最后会
            if int(file_id) > self.max_file_id:
                self.max_file_id = int(file_id)
            #
            # print('data_id: ' + file_id + ' coverage_percent:' + str(coverage_percent))
            continue

        # the last file may be restart related, it should be calculated too

        # final这里有点难理解，因为我们删掉了ORIGINAL_COVERAGE_FILE，
        # 原来生成覆盖度文件的时候，会在restart app前也生成一个覆盖度文件，命名方式为coverage_restart_2.ec，
        # 和30秒收集一次的文件命名方式不一样，所以做了特殊处理。
        # 这里我们删掉了ORIGINAL_COVERAGE_FILE，你可以理解成重复计算了最终覆盖度两次。不影响。
        # instruction_coverage_data['final']就是最后的覆盖度信息。
        self.generate_test_report(self.temp_path)
        instruction_coverage, branch_coverage, cxty_coverage, line_coverage, method_coverage, class_coverage, activity_coverage = self.get_coverage_data()
        instruction_coverage_data['final'] = instruction_coverage
        branch_coverage_data['final'] = branch_coverage
        cxty_coverage_data['final'] = cxty_coverage
        line_coverage_data['final'] = line_coverage
        method_coverage_data['final'] = method_coverage
        class_coverage_data['final'] = class_coverage
        activity_coverage_data['final'] = activity_coverage
        print('data_id: ' + 'final' + ' instruction_coverage:' + str(instruction_coverage))
        print('data_id: ' + 'final' + ' branch_coverage:' + str(branch_coverage))
        print('data_id: ' + 'final' + ' cxty_coverage:' + str(cxty_coverage))
        print('data_id: ' + 'final' + ' line_coverage:' + str(line_coverage))
        print('data_id: ' + 'final' + ' method_coverage:' + str(method_coverage))
        print('data_id: ' + 'final' + ' class_coverage:' + str(class_coverage))
        print('data_id: ' + 'final' + ' activity_coverage:' + str(activity_coverage))
        return instruction_coverage_data, branch_coverage_data, cxty_coverage_data, line_coverage_data, method_coverage_data, class_coverage_data, activity_coverage_data

    def save_curve_data(self, instruction_coverage_data, branch_coverage_data, cxty_coverage_data, line_coverage_data,
                        method_coverage_data, class_coverage_data, activity_coverage_data):
        # 最后会把每30秒的覆盖度信息写到curve_data_all这个文件。
        # 这是为了了解覆盖度在每个时间阶段的情况。
        print(instruction_coverage_data)
        sorted_instruction_data = collections.OrderedDict(instruction_coverage_data)
        print(instruction_coverage_data)
        sorted_branch_data = collections.OrderedDict(branch_coverage_data)
        sorted_cxty_data = collections.OrderedDict(cxty_coverage_data)
        sorted_line_data = collections.OrderedDict(line_coverage_data)
        sorted_method_data = collections.OrderedDict(method_coverage_data)
        sorted_class_data = collections.OrderedDict(class_coverage_data)
        sorted_activity_data = collections.OrderedDict(activity_coverage_data)
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        with open(os.path.join(self.report_path, 'curve_data_all.txt'), 'w') as f:
            for data_id in sorted_instruction_data:
                if data_id == 'final':
                    f.write('time: ' + 'final' + '\t' + 'instruction_coverage: ' + str(
                        round(sorted_instruction_data[data_id], 4)) + '\t')
                    f.write('branch_coverage: ' + str(round(sorted_branch_data[data_id], 4)) + '\t')
                    f.write('cxty_coverage: ' + str(round(sorted_cxty_data[data_id], 4)) + '\t')
                    f.write('line_coverage: ' + str(round(sorted_line_data[data_id], 4)) + '\t')
                    f.write('method_coverage: ' + str(round(sorted_method_data[data_id], 4)) + '\t')
                    f.write('class_coverage: ' + str(round(sorted_class_data[data_id], 4)) + '\t')
                    f.write('activity_coverage: ' + str(round(sorted_activity_data[data_id], 4)) + '\n')
                else:
                    f.write('time: ' + str(int(data_id) * self.time_interval) + '\t' + 'instruction_coverage: ' + str(
                        round(sorted_instruction_data[data_id], 4)) + '\t')
                    f.write('branch_coverage: ' + str(round(sorted_branch_data[data_id], 4)) + '\t')
                    f.write('cxty_coverage: ' + str(round(sorted_cxty_data[data_id], 4)) + '\t')
                    f.write('line_coverage: ' + str(round(sorted_line_data[data_id], 4)) + '\t')
                    f.write('method_coverage: ' + str(round(sorted_method_data[data_id], 4)) + '\t')
                    f.write('class_coverage: ' + str(round(sorted_class_data[data_id], 4)) + '\t')
                    f.write('activity_coverage: ' + str(round(sorted_activity_data[data_id], 4)) + '\n')
            f.write('===========================\n')
            # 这里你可以看到统计30min之内的覆盖度信息用的是sorted_instruction_data[MAX_ID / 2]，
            # 前面说到MAX_ID是有覆盖度文件的个数，所以除以2就是中间时刻的信息，因为原来都是跑60min。
            # 也就是说，如果你跑20min，那么MAX_ID / 2就是10min之内的信息。
            f.write(
                f"{self.max_file_id // 4}min:\tinstruction_coverage: {round(sorted_instruction_data[self.max_file_id // 2], 4)}\t")
            f.write('branch_coverage: ' + str(round(sorted_branch_data[self.max_file_id // 2], 4)) + '\t')
            f.write('cxty_coverage: ' + str(round(sorted_cxty_data[self.max_file_id // 2], 4)) + '\t')
            f.write('line_coverage: ' + str(round(sorted_line_data[self.max_file_id // 2], 4)) + '\t')
            f.write('method_coverage: ' + str(round(sorted_method_data[self.max_file_id // 2], 4)) + '\t')
            f.write('class_coverage: ' + str(round(sorted_class_data[self.max_file_id // 2], 4)) + '\t')
            f.write('activity_coverage: ' + str(round(sorted_activity_data[self.max_file_id // 2], 4)) + '\n')

            f.write(f"{self.max_file_id / 2}min:\tinstruction_coverage: {round(sorted_instruction_data['final'], 4)}\t")
            f.write('branch_coverage: ' + str(round(sorted_branch_data['final'], 4)) + '\t')
            f.write('cxty_coverage: ' + str(round(sorted_cxty_data['final'], 4)) + '\t')
            f.write('line_coverage: ' + str(round(sorted_line_data['final'], 4)) + '\t')
            f.write('method_coverage: ' + str(round(sorted_method_data['final'], 4)) + '\t')
            f.write('class_coverage: ' + str(round(sorted_class_data['final'], 4)) + '\t')
            f.write('activity_coverage: ' + str(round(sorted_activity_data['final'], 4)) + '\n')

        # 删除临时文件夹
        if os.path.exists(self.temp_path):
            shutil.rmtree(self.temp_path)

        # 将生成的测试报告移动到report目录
        test_report_path = os.path.join(self.app_source_path, 'build', 'reports', 'jacoco',
                                        'jacocoTestReportMergeWithParameter')
        shutil.move(test_report_path, self.report_path)


if __name__ == '__main__':
    time_interval = 30
    ca = CoverageAnalysis(1, 1, 57, time_interval)
    from Model.Result import Result

    result = Result(57, 'ss')
    ca.output_coverage_report(result)

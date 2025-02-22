import extmem
from basic_method import generator
from basic_method import WriteRtoDisk
from basic_method import WriteStoDisk


def liner_select(buffer):
    num = 0
    for i in range(16):
        addr = "r" + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            a = int(buffer.data[n][2 * j])
            b = int(buffer.data[n][2 * j + 1])
            if (a == 40):
                print("Relation_R", a, b)
                num += 1
                buffer.data[1].append(a)
                buffer.data[1].append(b)
                if num % 7 == 0:
                    buffer.writeBlockToDisk("liner_selection_result_R" + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    if num % 7 != 0:
        buffer.writeBlockToDisk("liner_selection_result_R" + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)
    num = 0
    for i in range(32):
        addr = "s" + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            c = int(buffer.data[n][2 * j])
            d = int(buffer.data[n][2 * j + 1])
            if (c == 60):
                print("Relation_S", c, d)
                num += 1
                buffer.data[1].append(c)
                buffer.data[1].append(d)
                if num % 7 == 0:
                    buffer.writeBlockToDisk("liner_selection_result_S" + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    if num % 7 != 0:
        buffer.writeBlockToDisk("liner_selection_result_S" + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)


def get_bufferdata(buffer, x):
    return int(buffer.data[x // 7][2 * (x % 7)])


def swap_bufferdata(buffer, b1, d1, b2, d2):
    t1 = buffer.data[b2][d2 * 2]
    t2 = buffer.data[b2][d2 * 2 + 1]
    buffer.data[b2][d2 * 2] = buffer.data[b1][d1 * 2]
    buffer.data[b2][d2 * 2 + 1] = buffer.data[b1][d1 * 2 + 1]
    buffer.data[b1][d1 * 2] = t1
    buffer.data[b1][d1 * 2 + 1] = t2


def sort_buffer(buffer):
    for i in range(55):
        for j in range(55 - i):
            if int(get_bufferdata(buffer, j)) > int(get_bufferdata(buffer, j + 1)):
                swap_bufferdata(buffer, j // 7, j % 7, (j + 1) // 7, (j + 1) % 7)


def low_bound(buffer, key, first, len):
    while len > 0:
        half = len // 2
        middle = first + half
        if get_bufferdata(buffer, middle) < key:
            first = middle + 1
            len = len - half - 1
        else:
            len = half
    return first


def merge_sort_forR(buffer):
    for i in range(8):
        buffer.freeBlockInBuffer(i)
    # 先读八块排好八块
    for i in range(8):
        buffer.readBlockFromDisk("r" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_R" + str(i), i)
    # 再读八块排好八块
    for i in range(8, 16):
        buffer.readBlockFromDisk("r" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_R" + str(i + 8), i)
    # 二路归并合并（这里只用了三块）
    counter = 0
    file1 = 0
    file2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("sort_R" + str(file1))
    b2 = buffer.readBlockFromDisk("sort_R" + str(file2 + 8))
    n = buffer.getNewBlockInBuffer()
    result_num = 0
    while file1 != 8 and file2 != 8:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        counter += 1
        if i == 7:
            file1 += 1
            i = 0
            if file1 < 8:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("sort_R" + str(file1))
        if j == 7:
            file2 += 1
            j = 0
            if file2 < 8:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("sort_R" + str(file2 + 8))
        if counter % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if file1 == 8:
        while file2 != 8:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            counter += 1
            if j == 7:
                file2 += 1
                j = 0
                if file2 < 8:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("sort_R" + str(file2 + 8))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif file2 == 8:
        while file1 != 8:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            counter += 1
            if i == 7:
                file1 += 1
                i = 0
                if file1 < 8:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("sort_R" + str(file1))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_search_forR(buffer):
    key = 40
    counter = 0
    result_num = 0
    for i in range(4):
        buffer.getNewBlockInBuffer()
    n = buffer.getNewBlockInBuffer()
    for k in range(4):
        for i in range(4):
            buffer.freeBlockInBuffer(i)
            buffer.readBlockFromDisk("binary_selection_temp_R" + str(4 * k + i))
        if key > get_bufferdata(buffer, 27) or key < get_bufferdata(buffer, 0):
            continue
        first = 0
        len = 28
        l1 = low_bound(buffer, 40, first, len)
        l2 = low_bound(buffer, 41, first, len)
        for i in range(l1, l2):
            a = buffer.data[i // 7][2 * (i % 7)]
            b = buffer.data[i // 7][2 * (i % 7) + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            print("Relation_R", a, b)
            counter += 1
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_result_R" + str(result_num), n)
                result_num += 1
                n = buffer.getNewBlockInBuffer()
    if counter % 7 != 0:
        buffer.writeBlockToDisk("binary_selection_result_R" + str(result_num), n)
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def temp_merge_S(buffer, p1, p2, result_num):
    counter = 0
    file1 = 0
    file2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("sort_S" + str(file1 + p1))
    b2 = buffer.readBlockFromDisk("sort_S" + str(file2 + p2))
    n = buffer.getNewBlockInBuffer()
    while file1 != 8 and file2 != 8:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        counter += 1
        if i == 7:
            file1 += 1
            i = 0
            if file1 < 8:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("sort_S" + str(file1 + p1))
        if j == 7:
            file2 += 1
            j = 0
            if file2 < 8:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("sort_S" + str(file2 + p2))
        if counter % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if file1 == 8:
        while file2 != 8:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            counter += 1
            if j == 7:
                file2 += 1
                j = 0
                if file2 < 8:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("sort_S" + str(file2 + p2))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif file2 == 8:
        while file1 != 8:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            counter += 1
            if i == 7:
                file1 += 1
                i = 0
                if file1 < 8:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("sort_S" + str(file1 + p1))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def merge_sort_forS(buffer):
    for i in range(8):
        buffer.freeBlockInBuffer(i)
    # 先排好八块
    for i in range(8):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i), i)
    # 再排好八块
    for i in range(8, 16):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 8), i)
    # 再排好八块
    for i in range(16, 24):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 16), i)
    # 最后排好八块
    for i in range(24, 32):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 24), i)
    # merge sort S
    temp_merge_S(buffer, 0, 8, 0)  # 合并0-16块
    temp_merge_S(buffer, 16, 24, 16)  # 合并16-32块
    # 再进行一次二路归并
    result_num = 0
    counter = 0
    file1 = 0
    file2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file1))
    b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file2 + 16))
    n = buffer.getNewBlockInBuffer()
    while file1 != 16 and file2 != 16:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        counter += 1
        if i == 7:
            file1 += 1
            i = 0
            if file1 < 16:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file1))
        if j == 7:
            file2 += 1
            j = 0
            if file2 < 16:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file2 + 16))
        if counter % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if file1 == 16:
        while file2 != 16:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            counter += 1
            if j == 7:
                file2 += 1
                j = 0
                if file2 < 16:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file2 + 16))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif file2 == 16:
        while file1 != 16:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            counter += 1
            if i == 7:
                file1 += 1
                i = 0
                if file1 < 16:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(file1))
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_search_forS(buffer):
    key = 60
    counter = 0
    result_num = 0
    for i in range(4):
        buffer.getNewBlockInBuffer()
    n = buffer.getNewBlockInBuffer()
    for k in range(8):
        for i in range(4):
            buffer.freeBlockInBuffer(i)
            buffer.readBlockFromDisk("binary_selection_temp2_S" + str(4 * k + i))
        if key > get_bufferdata(buffer, 27) or key < get_bufferdata(buffer, 0):
            continue
        first = 0
        len = 28
        l1 = low_bound(buffer, key, first, len)
        l2 = low_bound(buffer, key + 1, first, len)
        for i in range(l1, l2):
            a = buffer.data[i // 7][2 * (i % 7)]
            b = buffer.data[i // 7][2 * (i % 7) + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            print("Relation_S", a, b)
            counter += 1
            if counter % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_result_S" + str(result_num), n)
                result_num += 1
                n = buffer.getNewBlockInBuffer()
    if counter % 7 != 0:
        buffer.writeBlockToDisk("binary_selection_result_S" + str(result_num), n)
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_selection(buffer):
    merge_sort_forR(buffer)
    binary_search_forR(buffer)
    merge_sort_forS(buffer)
    binary_search_forS(buffer)
    # for i in range(16):
    #     extmem.dropBlockOnDisk("sort_R" + str(i))
    # for i in range(32):
    #     extmem.dropBlockOnDisk("sort_S" + str(i))
    # for i in range(16):
    #     extmem.dropBlockOnDisk("binary_selection_temp_R" + str(i))
    # for i in range(32):
    #     extmem.dropBlockOnDisk("binary_selection_temp_S" + str(i))
    #     extmem.dropBlockOnDisk("binary_selection_temp2_S" + str(i))


def project(buffer, relation, attribute):
    # 确定关系及其属性
    if attribute == 'A' or attribute == 'a' or attribute == 'C' or attribute == 'c':
        index_attribute = 0
    else:
        index_attribute = 1

    # 利用前面二分查询中已经排序好了的磁盘块，如果没有可以调用merge_sort_R和merge_sort_S
    if relation == 'R':
        num = 16
        begin = "binary_selection_temp_R"
    else:
        num = 32
        begin = "binary_selection_temp2_S"

    # 投影,利用已经排序好的数据去重
    counter = 0
    n = buffer.getNewBlockInBuffer()
    for i in range(num):
        m = buffer.readBlockFromDisk(begin + str(i))
        if i == 0:
            preattr = buffer.data[m][0 + index_attribute]
        for j in range(7):
            attr = buffer.data[m][2 * j + index_attribute]
            if i == 0 and j == 0:
                buffer.data[n].append(attr)
                print("Project:" + relation, "Attribute:" + attribute, attr)
                counter += 1
            else:
                if attr != preattr:
                    buffer.data[n].append(attr)
                    print("Project:" + relation, "Attribute:" + attribute, attr)
                    counter += 1
                    preattr = attr
                else:
                    counter += 1

        buffer.freeBlockInBuffer(m)
        if counter % 14 == 0:
            buffer.writeBlockToDisk("project" + str((counter - 1) // 14), n)
            n = buffer.getNewBlockInBuffer()


def nest_loop_join(buffer):
    print("nest_loop_join:")
    counter = 0
    # 分一块缓存用来写结果，一块外层循环，六块内层循环
    k = buffer.getNewBlockInBuffer()
    arr_num = buffer.numFreeBlk - 2
    for i in range(16 // arr_num + 1):
        for x in range(arr_num):
            buffer.freeBlockInBuffer(x + 1)
        mlist = []
        for l in range(arr_num):
            if i * 6 + l < 16:
                m = int(buffer.readBlockFromDisk("r" + str(i * 6 + l)))
                mlist.append(m)
        for j in range(32):  # 外层循环
            n = buffer.readBlockFromDisk("s" + str(j))
            for m in mlist:  # 内层循环
                for ii in range(7):
                    for jj in range(7):
                        if buffer.data[m][ii * 2] == buffer.data[n][jj * 2]:
                            a = buffer.data[m][ii * 2]
                            b = buffer.data[m][ii * 2 + 1]
                            c = buffer.data[n][jj * 2]
                            d = buffer.data[n][jj * 2 + 1]
                            print(a, b, d)
                            buffer.data[k].append(a)
                            buffer.data[k].append(b)
                            buffer.data[k].append(c)
                            buffer.data[k].append(d)
                            counter += 4
                            if counter % 12 == 0:
                                buffer.data[k].append(0)
                                buffer.data[k].append(0)
                                buffer.data[k].append(0)
                                buffer.data[k].append(counter / 12)
                                buffer.writeBlockToDisk("nest_loop_join_result" + str((counter - 1) // 12), k)
                                k = buffer.getNewBlockInBuffer()
            buffer.freeBlockInBuffer(n)
    if counter % 12 != 0:
        buffer.writeBlockToDisk("nest_loop_join_result" + str((counter - 1) / 12), k)
    buffer.freeBlockInBuffer(k)


def sort_merge_join(buffer):
    print("sort_merge_join:")
    # merge_sort_R(buffer)
    # merge_sort_S(buffer)
    # 利用前面二分搜索排序完的文件
    filename1 = "binary_selection_temp_R"
    filename2 = "binary_selection_temp2_S"

    # 块数仍然是6:1:1分配
    m = int(buffer.readBlockFromDisk(filename1 + "0"))
    arr_num = 6
    nlist = []
    l = 0
    for i in range(arr_num):
        n = int(buffer.readBlockFromDisk(filename2 + str(i)))
        nlist.append(n)

    # 用来写的buffer块
    k = buffer.getNewBlockInBuffer()

    # 计数器
    counter = 0

    # 记录文件数
    f1 = 0
    f2 = 0
    i = 0
    j = 0
    pre_f1 = f1
    pre_i = i
    pre_f2 = f2
    pre_j = j
    flag = False
    clear = False
    n = nlist[f2]
    before_a = 0

    # 扫描R和S一遍
    while True:
        a = int(buffer.data[m][2 * i])
        b = int(buffer.data[m][2 * i + 1])
        c = int(buffer.data[n][2 * j])
        d = int(buffer.data[n][2 * j + 1])
        if a != before_a:
            before_a = a
            pre_i = i
            pre_f1 = f1
        # 需要回溯的情况
        if flag and not a == c or clear:
            if not clear:
                flag = False
                i += 1
                j = pre_j
                f2 = pre_f2
                n = nlist[f2]
            # 清空了六块的情况
            else:
                if flag:
                    flag = False
                    j = pre_j
                    f2 = pre_f2
                    n = nlist[f2]
                    while True:
                        a = int(buffer.data[m][2 * i])
                        b = int(buffer.data[m][2 * i + 1])
                        c = int(buffer.data[n][2 * j])
                        d = int(buffer.data[n][2 * j + 1])
                        if a < c:
                            i += 1
                        elif a > c:
                            j += 1
                            break
                        else:
                            buffer.data[k].append(a)
                            buffer.data[k].append(b)
                            buffer.data[k].append(c)
                            buffer.data[k].append(d)
                            print(a, b, d)
                            flag = True
                            j += 1
                            counter += 4
                            if counter % 12 == 0:
                                buffer.writeBlockToDisk("sort_merge_join_result" + str((counter - 1) // 12), k)
                                k = buffer.getNewBlockInBuffer()
                        if i == 7:
                            i = 0
                            f1 += 1
                            if f1 < 16:
                                buffer.freeBlockInBuffer(m)
                                m = buffer.readBlockFromDisk(filename1 + str(f1))
                            else:
                                break
                        if j == 7:
                            j = 0
                            f2 += 1
                            if f2 < len(nlist):
                                n = nlist[f2]
                            else:
                                i += 1
                                j = pre_j
                                f2 = pre_f2
                                n = nlist[f2]
                                if i == 7:
                                    i = 0
                                    f1 += 1
                                    if f1 < 16:
                                        buffer.freeBlockInBuffer(m)
                                        m = buffer.readBlockFromDisk(filename1 + str(f1))
                                    else:
                                        break
                clear = False
                f2 = 0
                pre_f2 = 0
                pre_j = 0
                j = 0
                buffer.freeBlockInBuffer(m)
                m = buffer.readBlockFromDisk(filename1 + str(pre_f1))
                i = pre_i
                f1 = pre_f1
                pre_f1 = 0
                pre_i = 0
                for n in nlist:
                    buffer.freeBlockInBuffer(n)
                nlist = []
                if l < 32 // arr_num + 1:
                    for p in range(arr_num):
                        if l * arr_num + p < 32:
                            n = int(buffer.readBlockFromDisk(filename2 + str(l * arr_num + p)))
                            nlist.append(n)
                    n = nlist[f2]
                else:
                    break
                continue
        elif a < c:
            i += 1
        elif a > c:
            j += 1
        else:
            buffer.data[k].append(a)
            buffer.data[k].append(b)
            buffer.data[k].append(c)
            buffer.data[k].append(d)
            print(a, b, d)
            if not flag:
                pre_f2 = f2
                pre_j = j
            flag = True
            j += 1
            counter += 4
            if counter % 12 == 0:
                buffer.writeBlockToDisk("sort_merge_join_result" + str((counter - 1) // 12), k)
                k = buffer.getNewBlockInBuffer()
        if i == 7:
            i = 0
            f1 += 1
            if f1 < 16:
                buffer.freeBlockInBuffer(m)
                m = buffer.readBlockFromDisk(filename1 + str(f1))
            else:
                break
        if j == 7:
            j = 0
            f2 += 1
            if f2 < len(nlist):
                n = nlist[f2]
            else:
                i += 1
                l += 1
                clear = True
                if i == 7:
                    i = 0
                    f1 += 1
                    if f1 < 16:
                        buffer.freeBlockInBuffer(m)
                        m = buffer.readBlockFromDisk(filename1 + str(f1))
                    else:
                        break
    # 保存最后一块
    if counter % 12 != 0:
        buffer.writeBlockToDisk("sort_merge_join_result" + str((counter - 1) // 12), k)

    # 删掉暂存文件
    filename3 = "binary_selection_temp_S"
    for i in range(16):
        extmem.dropBlockOnDisk(filename1 + str(i))
    for i in range(32):
        extmem.dropBlockOnDisk(filename2 + str(i))
        extmem.dropBlockOnDisk(filename3 + str(i))
    for i in range(16):
        extmem.dropBlockOnDisk("sort_R" + str(i))
    for i in range(32):
        extmem.dropBlockOnDisk("sort_S" + str(i))


def hash_join(buffer):
    print("hash_join:")
    dictforR = {}
    dictforS = {}
    filename1 = "r"
    filename2 = "s"
    hash = 10
    # 构造R的哈希
    for i in range(16):
        m = int(buffer.readBlockFromDisk(filename1 + str(i)))
        for j in range(7):
            a = int(buffer.data[m][2 * j])
            if a % hash in dictforR.keys():
                dictforR[a % hash].append((i, j))
            else:
                dictforR[a % hash] = []
                dictforR[a % hash].append((i, j))
        buffer.freeBlockInBuffer(m)
    # 构造S的哈希
    for i in range(32):
        n = int(buffer.readBlockFromDisk(filename2 + str(i)))
        for j in range(7):
            c = int(buffer.data[n][2 * j])
            # d = buffer.data[n][2 * j + 1]
            if c % hash in dictforS.keys():
                dictforS[c % hash].append((i, j))
            else:
                dictforS[c % hash] = []
                dictforS[c % hash].append((i, j))
        buffer.freeBlockInBuffer(n)
    # 在哈希桶内排序
    for h in range(hash):
        if h in dictforR.keys():
            dictforR[h] = sorted(dictforR[h])
        if h in dictforS.keys():
            dictforS[h] = sorted(dictforS[h])
    cnt = 0
    # 用来写的块
    k = buffer.getNewBlockInBuffer()
    # 在哈希桶内连接
    for h in range(hash):
        for i in range(8):
            buffer.freeBlockInBuffer(i)
        if h not in dictforR.keys() or h not in dictforS.keys():
            continue
        listR = dictforR[h]
        listS = dictforS[h]
        for i, r in enumerate(listR):
            x = r[1]
            m = buffer.readBlockFromDisk(filename1 + str(r[0]))
            a = buffer.data[m][2 * x]
            b = buffer.data[m][2 * x + 1]
            for j, s in enumerate(listS):
                y = s[1]
                n = buffer.readBlockFromDisk(filename2 + str(s[0]))
                c = buffer.data[n][2 * y]
                d = buffer.data[n][2 * y + 1]
                if a == c:
                    buffer.data[k].append(a)
                    buffer.data[k].append(b)
                    buffer.data[k].append(c)
                    buffer.data[k].append(d)
                    print(a, b, d)
                    cnt += 4
                    if cnt % 12 == 0:
                        buffer.writeBlockToDisk("hash_join_result" + str((cnt - 1) // 12), k)
                        k = buffer.getNewBlockInBuffer()
                buffer.freeBlockInBuffer(n)
            buffer.freeBlockInBuffer(m)
    # 保存最后一块
    if cnt % 12 != 0:
        buffer.writeBlockToDisk("hash_join_result" + str((cnt - 1) // 12), k)
    buffer.freeBlockInBuffer(k)


if __name__ == '__main__':
    # 构造buffer
    buffer = extmem.Buffer(520, 64)

    # 构造数据
    R, S = generator()
    WriteRtoDisk(buffer, R)
    WriteStoDisk(buffer, S)

    # 线性查询
    liner_select(buffer)

    # 二分查询
    binary_selection(buffer)

    # 投影
    project(buffer, "R", "A")

    # Nested-Loop Join
    buffer.freeBuffer()
    print()
    nest_loop_join(buffer)

    # sort-merge-join
    buffer.freeBuffer()
    print()
    sort_merge_join(buffer)

    # hash-join
    buffer.freeBuffer()
    print()
    hash_join(buffer)

    print()
    buffer.freeBuffer()

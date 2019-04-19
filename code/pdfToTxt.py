#-*-encoding:utf8-*-#
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from cStringIO import StringIO
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed, PDFPage
import re
result = []
class Pdf2TxtManager:
    def __init__(self):
        pass

    def convert_pdf_2_text(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        with open('../pdf/' + path, 'rb') as fp:
            pagecnt = 0
            for page in PDFPage.get_pages(fp, set()):
                interpreter.process_page(page)
                pagecnt += 1
                if pagecnt == 3:
                    break
            text = retstr.getvalue()
        device.close()
        retstr.close()
        return text

    def changePdfToTxt(self, fileName):
        pageNum, page_context = self.readPdfInPages(fileName)
        #exit(0)
        file_num = pageNum / 100
        if pageNum % 100 > 0:
            file_num += 1
        for i in range(file_num):
            lowb = i * 100
            upb = min((i + 1) * 100 + 2, pageNum)
            print lowb, upb
            resFile = '../result/' + fileName.replace(".pdf", "_%d_%d.txt" % (lowb, upb - 1))
            with open(resFile, "w") as f:
                for pageNo in range(lowb, upb):
                    #print pageNo
                    for paragraph in page_context[pageNo]:
                        sentences = paragraph.split(u"。")
                        for s in sentences:
                            s = s.strip()
                            if not len(s):
                                continue
                            f.write(s + "\n")
                    f.write(">>>>>>>>>>>>>>>>>>>>>>>Page %d Finish>>>>>>>>>>>>>>>>>>>>>>>\n" % (pageNo + 1))
                print "result File %s write finish" % (resFile)
        print "process End"

    def readPdfInPages(self, fileName):
        file = open('../pdf/' + fileName, 'rb') #二进制读
        praser = PDFParser(file) #创建pdf文档分析器
        doc = PDFDocument(praser) #创建一个pdf文档
        #链接文档与分析器
        #praser.set_document(doc)
        #doc.set_parser(praser)

        #提供初始化密码,没有就创建一个空的字符串
        #doc.initialize()

        if not doc.is_extractable: #检测文档是否提供txt转换
            raise PDFTextExtractionNotAllowed ##使用raise显示地引发异常，后续不再执行
        else:
            #PDF资源管理器
            pdfRsrcmgr = PDFResourceManager()
            #创建一个PDF设备对象
            laparmas = LAParams()
            device = PDFPageAggregator(pdfRsrcmgr, laparams=laparmas)
            #PDF解释器对象
            interpreter = PDFPageInterpreter(pdfRsrcmgr, device)

            pages_context = [] ##准备按页缓存数据
            #遍历列表，每次处理一个page的内容
            pagecnt = 0
            last_page_endl = True ##前一页的内容正常结束
            last_row_endl = True  ##本页前一行正常结束
            for page in PDFPage.create_pages(doc):
                pages_context.append([])  ## a new page
                interpreter.process_page(page)
                ##接受该页的LTPage对象

                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox,
                # LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                layout_cnt = 0
                layout_max = 0
                text_layout = []
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        layout_max += 1
                        text_layout.append(x)
                if len(text_layout):
                    del text_layout[0]
                    layout_max -= 1

                for x in text_layout:
                    layout_cnt += 1
                    if layout_cnt == layout_max:  ##本页文本扫完
                        if len(x.get_text()) > 15:
                            print "Page%d" % pagecnt, x.get_text(), last_row_endl, last_page_endl
                        last_page_endl = last_row_endl
                        break

                    text = x.get_text()
                    if text.find(" \n"):  ##包含某段话的结尾
                        texts = text.split(" \n")
                        for idx in range(len(texts)):
                            if idx == len(texts) - 1:
                                endl = False
                            else:
                                endl = True
                            last_row_endl, last_page_endl = self.addNewSentence(texts[idx], last_row_endl,
                                                            last_page_endl, pagecnt, pages_context, endl)
                    else:
                        last_row_endl, last_page_endl = self.addNewSentence(text, last_row_endl,
                                                                            last_page_endl, pagecnt, pages_context,
                                                                            endl=False)
                #print layout_cnt, layout_max
                #print "page %d finish" % (pagecnt + 1)
                pagecnt += 1
                #if pagecnt == 4:
                #    break
                if pagecnt % 100 == 0:
                    print u"已处理%d页数据 " % (pagecnt)
            print "process end!"
            return pagecnt, pages_context

    def addNewSentence(self, text, last_row_endl, last_page_endl, pagecnt, pages_context, endl):
        text = "".join(text.split("\n"))
        text = text.strip()
        if len(text) == 0:
            return last_row_endl, last_page_endl
        # print "Page%d" % pagecnt, x.get_text(), last_row_endl, last_page_endl

        if last_row_endl:  # 上一行结束了
            pages_context[pagecnt].append(text)  ##新起一行
            last_row_endl = endl
        elif last_page_endl:  # 上一行没结束但是上一页结束了
            pages_context[pagecnt][-1] += text
            last_row_endl = endl
        else:  ##上一页的最后一行没结束
            try:
                pages_context[self.lastPage(pages_context, pagecnt)][-1] += text
            except:
                print pagecnt, text
                exit(0)
            last_page_endl = endl
            last_row_endl = endl
        return last_row_endl, last_page_endl

    def lastPage(self, pages_context, pagecnt):
        while pagecnt >= 1:
            pagecnt -= 1
            if len(pages_context[pagecnt]):
                return pagecnt
        for i in range(len(pages_context)):
            print "Page %d has rows %d" % (i, len(pages_context[i]))



if __name__=="__main__":
    file_name = "P020190417560516474414.pdf"
    #file_name = "科大讯飞招股说明书.pdf"
    task = Pdf2TxtManager()
    task.changePdfToTxt(fileName=file_name)
    #text = task.convert_pdf_2_text(file_name)
    #print type(text)
    #print text

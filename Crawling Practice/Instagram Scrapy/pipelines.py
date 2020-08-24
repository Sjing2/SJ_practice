# 어떤 데이터를 필터링 한다던지, 아니면 데이터 입력을 한다던지 하는 후처리를 여기서 진행

class TutorialPipeline(object) :
    def process_item(self, item, spider):
        return item
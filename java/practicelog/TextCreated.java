package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.TextDTO;

public class TextCreated implements PracticeLogBody {

    public TextDTO created;

    public TextCreated() {
    }

    public TextCreated(TextDTO created) {
        this.created = created;
    }
}

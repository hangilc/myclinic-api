package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.RoujinDTO;

public class RoujinDeleted implements PracticeLogBody {

    public RoujinDTO deleted;

    public RoujinDeleted() {
    }

    public RoujinDeleted(RoujinDTO deleted) {
        this.deleted = deleted;
    }
}
package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.RoujinDTO;

public class RoujinUpdated implements PracticeLogBody {

    public RoujinDTO prev;
    public RoujinDTO updated;

    public RoujinUpdated() {
    }

    public RoujinUpdated(RoujinDTO prev, RoujinDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
package dev.myclinic.dto;

public class ShinryouFullWithAttrDTO {

    public ShinryouFullDTO shinryou;
    public ShinryouAttrDTO attr;

    public static ShinryouFullWithAttrDTO create(ShinryouFullDTO shinryou, ShinryouAttrDTO attr){
        ShinryouFullWithAttrDTO result = new ShinryouFullWithAttrDTO();
        result.shinryou = shinryou;
        result.attr = attr;
        return result;
    }
}

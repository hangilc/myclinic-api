package dev.myclinic.dto;

import java.util.List;

public class EnterConductByNamesRequestDTO {
    public int kind;
    public String gazouLabel;
    public List<String> shinryouNames;
    public List<EnterConductKizaiByNamesRequestDTO> kizaiList;

    @Override
    public String toString() {
        return "EnterConductByNamesRequestDTO{" +
                "kind=" + kind +
                ", gazouLabel='" + gazouLabel + '\'' +
                ", shinryouNames=" + shinryouNames +
                ", kizaiList=" + kizaiList +
                '}';
    }
}

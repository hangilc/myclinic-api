package dev.myclinic.dto;

import java.util.List;

public class IntraclinicPostPageDTO {
    public int totalPages;
    public List<IntraclinicPostDTO> posts;

    @Override
    public String toString() {
        return "IntraclinicPostPageDTO{" +
                "totalPages=" + totalPages +
                ", posts=" + posts +
                '}';
    }
}

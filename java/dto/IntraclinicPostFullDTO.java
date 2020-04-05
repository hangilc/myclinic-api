package dev.myclinic.dto;

import java.util.List;

public class IntraclinicPostFullDTO {
    public IntraclinicPostDTO post;
    public List<IntraclinicCommentDTO> comments;

    @Override
    public String toString() {
        return "IntraclinicPostFullDTO{" +
                "post=" + post +
                ", comments=" + comments +
                '}';
    }
}

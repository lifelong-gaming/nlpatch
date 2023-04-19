import ModelMetadata from "@/types/ModelMetadata";
import ModelMetadataCard from "@/components/ModelMetadataCard";
import Grid from '@mui/material/Unstable_Grid2';
import { Box } from "@mui/material";

interface Prop {
  modelMetadataList: ModelMetadata[];
  onStartDialogue: (id: string) => void;
}

const ModelMetadataCards = (props: Prop) => {
  const { modelMetadataList, onStartDialogue } = props;
  return (
    <Box sx={{ width: "100%"}}>
      <Grid container spacing={1}>
        {modelMetadataList.map((modelMetadata, idx) => (
          <Grid xs={12} md={6} lg={4} key={idx}>
            <ModelMetadataCard onStartDialogue={onStartDialogue} modelMetadata={modelMetadata} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ModelMetadataCards

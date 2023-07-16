import { Box, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import axios from "axios";

const SecondaryDraw = () => {
  const theme = useTheme();

  axios
    .get("http://127.0.0.1:8000/api/server/select/?category=gaming")
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });

  return (
    <Box
      sx={{
        mt: `${theme.primaryAppBar.height}px`,
        minWidth: `${theme.secondaryDraw.width}px`,
        height: `calc(100vh - ${theme.primaryAppBar.height}px )`,
        borderRight: `1px solid ${theme.palette.divider}`,
        display: { xs: "none", sm: "block" },
        overflowY: "auto",
      }}
    >
      {[...Array(50)].map((_, i) => (
        <Typography key={i} paragraph>
          {i + 1}
        </Typography>
      ))}
    </Box>
  );
};

export default SecondaryDraw;

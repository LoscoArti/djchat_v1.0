import { Box } from "@mui/material";
import { useTheme } from "@mui/material/styles";

type SecondaryDrawProps = {
  children: React.ReactNode;
};

const SecondaryDraw = ({ children }: SecondaryDrawProps) => {
  const theme = useTheme();

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
      {children}
    </Box>
  );
};

export default SecondaryDraw;

import { useMembershipContext } from "../../context/MemberContext";
import { useParams } from "react-router-dom";

const JoinServerButton = () => {
  const { serverId } = useParams();
  const { joinServer, leaveServer, isLoading, error, isUserMember } =
    useMembershipContext();

  const handleJoinServer = async () => {
    try {
      await joinServer(Number(serverId));
      console.log("User has joined server");
    } catch (error) {
      console.log("Error joining server", error);
    }
  };

  const handleLeaveServer = async () => {
    try {
      await leaveServer(Number(serverId));
      console.log("User has left the server seccessfully");
    } catch (error) {
      console.log("Error leaving the server", error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  // if (error) {
  //   return <div>{error.message}</div>;
  // }

  return (
    <>
      {isUserMember ? (
        <button onClick={handleLeaveServer}>Leave Server</button>
      ) : (
        <button onClick={handleJoinServer}>Join Server</button>
      )}
    </>
  );
};

export default JoinServerButton;

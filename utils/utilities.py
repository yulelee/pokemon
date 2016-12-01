# this file contains helper functions could be utilized my multiple modules

##################################### get_radar_region
# given the board size, and the radius of the radar, as well as the current 
# position of the agent, this function return a quadruple that contains
# the borders of the radar covered region on the board

def get_radar_region(agent_position, radar_radius, board_size):
	start_x = max(0, agent_position[0] - radar_radius)
	start_y = max(0, agent_position[1] - radar_radius)
	end_x = min(board_size, agent_position[0] + radar_radius)
	end_y = min(board_size, agent_position[1] + radar_radius)
	return (start_x, start_y, end_x, end_y)
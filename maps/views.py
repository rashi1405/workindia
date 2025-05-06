from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Map
from .serializers import MapSerializer
import json
from collections import deque


class MapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """List all maps for the user or return specific map if `id` is provided."""
        map_id = request.GET.get('id')
        if map_id:
            city_map = get_object_or_404(Map, id=map_id, owner=request.user)
            serializer = MapSerializer(city_map)
            return Response(serializer.data)
        else:
            maps = Map.objects.filter(owner=request.user)
            serializer = MapSerializer(maps, many=True)
            return Response(serializer.data)

    def post(self, request):
        """Create a new map."""
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = MapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update a map (must provide 'id')."""
        map_id = request.data.get('id')
        city_map = get_object_or_404(Map, id=map_id, owner=request.user)
        serializer = MapSerializer(city_map, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete a map (must provide 'id')."""
        map_id = request.data.get('id')
        city_map = get_object_or_404(Map, id=map_id, owner=request.user)
        city_map.delete()
        return Response({'detail': 'Map deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class MapNavigationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Determine if path exists using BFS from start to end."""
        try:
            map_id = request.GET.get('map_id')
            row_s = int(request.GET.get('row_s'))
            col_s = int(request.GET.get('col_s'))
            row_e = int(request.GET.get('row_e'))
            col_e = int(request.GET.get('col_e'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid or missing coordinates'}, status=status.HTTP_400_BAD_REQUEST)

        city_map = get_object_or_404(Map, id=map_id)
        if not city_map.public and city_map.owner != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        layout = city_map.layout

        def is_valid(r, c):
            return 0 <= r < len(layout) and 0 <= c < len(layout[0]) and layout[r][c] == "R"

        def bfs():
            visited = [[False] * len(layout[0]) for _ in range(len(layout))]
            queue = deque()
            queue.append((row_s, col_s))
            visited[row_s][col_s] = True

            while queue:
                r, c = queue.popleft()
                if (r, c) == (row_e, col_e):
                    return True
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if is_valid(nr, nc) and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
            return False

        if not is_valid(row_s, col_s) or not is_valid(row_e, col_e):
            return Response({'path_exists': False, 'reason': 'Start or end is blocked or out of bounds'})

        path_found = bfs()
        return Response({'path_exists': path_found})

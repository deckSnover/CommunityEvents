FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["CommunityEvents/CommunityEvents.csproj", "CommunityEvents/"]
RUN dotnet restore "CommunityEvents/CommunityEvents.csproj"
COPY . .
WORKDIR "/src/CommunityEvents"
RUN dotnet build "CommunityEvents.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "CommunityEvents.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "CommunityEvents.dll"]  
